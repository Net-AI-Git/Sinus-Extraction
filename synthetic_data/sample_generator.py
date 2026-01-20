"""
Sample generation orchestration for synthetic data.

This module provides functions to generate complete samples including signals,
noise, STFT spectrograms, and time-frequency representations. It orchestrates
the parameter generation, signal generation, and TF representation creation.

Why: Centralizing sample generation logic ensures consistent sample creation
across the codebase. This module coordinates parameter validation, signal
generation, and TF representation to produce complete training samples.

What: Provides functions to validate IF parameters, generate valid parameter
sets through retry logic, and create complete Sample objects with all required
data for training segmentation models.
"""

from typing import List, Tuple, Optional
import numpy as np
from pydantic import BaseModel, Field

from .config import SyntheticDataConfig
from .signal_models import (
    gen_poly_params,
    gen_coschirp_params,
    gen_step_sine_params,
    gen_freq_jump_params,
    gen_sawtooth_mod_params,
    gen_square_mod_params,
    gen_phase_jump_params,
    gen_amplitude_mod_params
)
from .signal_generators import (
    poly_signal_and_if,
    coschirp_signal_and_if,
    step_sine_signal_and_if,
    freq_jump_signal_and_if,
    sawtooth_mod_signal_and_if,
    square_mod_signal_and_if,
    phase_jump_signal_and_if,
    amplitude_mod_signal_and_if
)
from .signal_processing import awgn, stft_mag_128x8000
from .tf_representation import ifs_to_ideal_tf, generate_binary_mask
from .exceptions import InvalidParameterError, SignalGenerationError
import logging

logger = logging.getLogger(__name__)


class Sample(BaseModel):
    """
    Complete sample data structure for synthetic data generation.
    
    Why: Encapsulates all data associated with a single synthetic sample,
    providing a structured way to pass sample data between functions and
    ensuring all required fields are present.
    
    What: A Pydantic BaseModel containing all data for a synthetic sample:
    number of components, clean and noisy signals, STFT spectrogram,
    instantaneous frequencies, normalized IFs, ideal TF representation,
    and binary mask.
    
    Attributes:
        n_components: Number of signal components in this sample.
        x_clean: Clean signal without noise, shape [n_samples], dtype float32.
        x_noisy: Signal with added noise, shape [n_samples], dtype float32.
        stft: STFT magnitude spectrogram, shape [n_freq_bins, n_time_bins],
            dtype float32, values in [0, 1].
        ifs_hz: List of instantaneous frequency vectors in Hz, one per component,
            each shape [n_time_bins].
        ifs_norm: Normalized IF matrix, shape [n_components, n_time_bins],
            dtype float32, values in [0, 1] relative to fmax.
        tf_ideal: Ideal TF representation, shape [n_freq_bins, n_time_bins],
            dtype float32, values in [0, 1].
        binary_mask: Binary mask, shape [n_freq_bins, n_time_bins],
            dtype uint8, values in {0, 1}.
    """
    model_config = {"arbitrary_types_allowed": True}
    
    n_components: int = Field(description="Number of signal components")
    x_clean: np.ndarray = Field(description="Clean signal without noise")
    x_noisy: np.ndarray = Field(description="Signal with added noise")
    stft: np.ndarray = Field(description="STFT magnitude spectrogram")
    ifs_hz: List[np.ndarray] = Field(description="IF vectors in Hz per component")
    ifs_norm: np.ndarray = Field(description="Normalized IF matrix")
    tf_ideal: np.ndarray = Field(description="Ideal TF representation")
    binary_mask: np.ndarray = Field(description="Binary mask")
    signal_types: List[str] = Field(
        default=[],
        description="List of signal type names, one per component"
    )


def params_valid(
    IFs: List[np.ndarray],
    fmin: float = 0.0,
    fmax: float = 2000.0
) -> bool:
    """
    Validate that all IF vectors are within valid frequency range.
    
    Why: Parameter validation ensures generated signals have IF trajectories
    within the representable frequency range [0, fmax]. This prevents invalid
    samples that would cause errors in TF representation generation.
    
    What: Checks that all IF values in all IF vectors are within [fmin, fmax]
    and are finite (not NaN or Inf). Returns True if all IFs are valid,
    False otherwise.
    
    Args:
        IFs: List of IF vectors in Hz, one per signal component.
        fmin: Minimum valid frequency in Hz. Default 0.0.
        fmax: Maximum valid frequency (Nyquist) in Hz. Default 2000.0.
    
    Returns:
        bool: True if all IFs are within [fmin, fmax] and finite, False otherwise.
    """
    for IF in IFs:
        if np.any((IF < fmin) | (IF > fmax) | ~np.isfinite(IF)):
            return False
    return True


def _determine_signal_type(
    component_index: int,
    n_components: int
) -> str:
    """
    Determine signal type based on component index.
    
    Why: Provides a consistent mapping from component index to signal type,
    enabling scenario detection and organized signal generation.
    
    What: Maps component indices to signal types:
    - 0, 1: poly_phase
    - 2: cos_chirp
    - 3: step_sine
    - 4: freq_jump
    - 5: sawtooth_mod
    - 6: square_mod
    - 7: phase_jump
    - 8: amplitude_mod
    
    Args:
        component_index: Index of the component (0-based).
        n_components: Total number of components.
    
    Returns:
        str: Signal type name.
    """
    signal_map = {
        0: 'poly_phase',
        1: 'poly_phase',
        2: 'cos_chirp',
        3: 'step_sine',
        4: 'freq_jump',
        5: 'sawtooth_mod',
        6: 'square_mod',
        7: 'phase_jump',
        8: 'amplitude_mod'
    }
    return signal_map.get(component_index, 'poly_phase')


def _generate_component_signals(
    rng: np.random.Generator,
    n_components: int,
    t: np.ndarray,
    signal_scenario: Optional[str] = None,
    fmax: Optional[float] = None
) -> Tuple[List[np.ndarray], List[np.ndarray], List[str]]:
    """
    Generate signals and IFs for each component type.
    
    Why: Separates the component generation logic for clarity and testability.
    This function handles the conditional logic for generating different numbers
    of components with different signal types.
    
    What: Generates signals based on n_components (1-8):
    - 1-2 components: polynomial phase signals
    - 3 components: 2 polynomial + 1 cosine chirp
    - 4 components: 2 polynomial + 1 cosine chirp + 1 step sine
    - 5+ components: adds new signal types in order
    Returns lists of signal arrays, IF arrays, and signal type names.
    
    Args:
        rng: NumPy random number generator.
        n_components: Number of components to generate (1-8).
        t: Time vector in seconds.
        signal_scenario: Optional signal scenario name. If provided, generates
            only that signal type. Default None.
    
    Returns:
        Tuple[List[np.ndarray], List[np.ndarray], List[str]]: A tuple containing:
            - List of signal arrays, one per component.
            - List of IF arrays in Hz, one per component.
            - List of signal type names, one per component.
    
    Raises:
        ValueError: If n_components is not in [1, 8].
    """
    if not 1 <= n_components <= 8:
        raise ValueError(
            f"Number of components must be in [1, 8], got {n_components}."
        )
    
    xs, IFs, signal_types = [], [], []
    
    for i in range(n_components):
        if signal_scenario:
            sig_type = signal_scenario
        else:
            sig_type = _determine_signal_type(i, n_components)
        
        if sig_type == 'poly_phase':
            p = gen_poly_params(rng, fmax=fmax)
            x, IF = poly_signal_and_if(t, p)
        elif sig_type == 'cos_chirp':
            q = gen_coschirp_params(rng, fmax=fmax)
            x, IF = coschirp_signal_and_if(t, q)
        elif sig_type == 'step_sine':
            step_params = gen_step_sine_params(rng, freq_max=fmax if fmax else 1000.0)
            x, IF = step_sine_signal_and_if(t, step_params)
        elif sig_type == 'freq_jump':
            jump_params = gen_freq_jump_params(rng, freq_max=fmax if fmax else 2000.0)
            x, IF = freq_jump_signal_and_if(t, jump_params)
        elif sig_type == 'sawtooth_mod':
            sawtooth_params = gen_sawtooth_mod_params(
                rng, base_freq_range=(1.0, fmax if fmax else 2000.0)
            )
            x, IF = sawtooth_mod_signal_and_if(t, sawtooth_params)
        elif sig_type == 'square_mod':
            square_params = gen_square_mod_params(
                rng, base_freq_range=(1.0, fmax if fmax else 2000.0)
            )
            x, IF = square_mod_signal_and_if(t, square_params)
        elif sig_type == 'phase_jump':
            phase_params = gen_phase_jump_params(
                rng, base_freq_range=(1.0, fmax if fmax else 2000.0)
            )
            x, IF = phase_jump_signal_and_if(t, phase_params)
        elif sig_type == 'amplitude_mod':
            amp_params = gen_amplitude_mod_params(
                rng, base_freq_range=(1.0, fmax if fmax else 2000.0)
            )
            x, IF = amplitude_mod_signal_and_if(t, amp_params)
        else:
            p = gen_poly_params(rng, fmax=fmax)
            x, IF = poly_signal_and_if(t, p)
            sig_type = 'poly_phase'
        
        xs.append(x)
        IFs.append(IF)
        signal_types.append(sig_type)
    
    return xs, IFs, signal_types


def draw_valid_params_for_components(
    rng: np.random.Generator,
    n_components: int,
    t: np.ndarray,
    fmax: float,
    max_tries: int = 200,
    signal_scenario: Optional[str] = None
) -> Tuple[List[np.ndarray], List[np.ndarray], List[str]]:
    """
    Sample parameters until valid IF ranges are obtained.
    
    Why: Parameter sampling with validation ensures all generated samples have
    valid IF trajectories within the representable frequency range. Retry logic
    handles cases where random parameters produce invalid IFs.
    
    What: Attempts to generate valid component signals up to max_tries times.
    For each attempt, generates signals and IFs, validates the IFs are within
    [0, fmax], and returns if valid. If max_tries is exceeded, raises an exception.
    
    Args:
        rng: NumPy random number generator.
        n_components: Number of components to generate (1-8).
        t: Time vector in seconds.
        fmax: Maximum frequency (Nyquist) in Hz.
        max_tries: Maximum number of attempts to find valid parameters.
            Default 200.
        signal_scenario: Optional signal scenario name. Default None.
    
    Returns:
        Tuple[List[np.ndarray], List[np.ndarray], List[str]]: A tuple containing:
            - List of signal arrays, one per component.
            - List of IF arrays in Hz, one per component.
            - List of signal type names, one per component.
    
    Raises:
        SignalGenerationError: If valid parameters cannot be found within
            max_tries attempts.
    """
    # #region agent log
    import json
    import time
    log_path_local = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "O",
            "location": "sample_generator.py:draw_valid_params_for_components:ENTRY",
            "message": "Function entry",
            "data": {
                "n_components": n_components,
                "fmax": fmax,
                "max_tries": max_tries,
                "signal_scenario": signal_scenario,
                "t_length": len(t),
                "t_min": float(t.min()),
                "t_max": float(t.max())
            },
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path_local, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    for attempt in range(max_tries):
        xs, IFs, signal_types = _generate_component_signals(
            rng, n_components, t, signal_scenario, fmax=fmax
        )
        
        # #region agent log
        try:
            ifs_info = []
            for idx, IF in enumerate(IFs):
                ifs_info.append({
                    "component": idx,
                    "min": float(IF.min()),
                    "max": float(IF.max()),
                    "mean": float(IF.mean()),
                    "has_nan": bool(np.any(np.isnan(IF))),
                    "has_inf": bool(np.any(np.isinf(IF))),
                    "below_zero": bool(np.any(IF < 0.0)),
                    "above_fmax": bool(np.any(IF > fmax)),
                    "signal_type": signal_types[idx] if idx < len(signal_types) else "unknown"
                })
            
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "P",
                "location": "sample_generator.py:draw_valid_params_for_components:ATTEMPT",
                "message": "Parameter generation attempt",
                "data": {
                    "attempt": attempt + 1,
                    "max_tries": max_tries,
                    "n_components": n_components,
                    "fmax": fmax,
                    "ifs_info": ifs_info,
                    "is_valid": params_valid(IFs, fmin=0.0, fmax=fmax)
                },
                "timestamp": int(time.time() * 1000)
            }
            with open(log_path_local, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass
        # #endregion
        
        if params_valid(IFs, fmin=0.0, fmax=fmax):
            # #region agent log
            try:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "Q",
                    "location": "sample_generator.py:draw_valid_params_for_components:SUCCESS",
                    "message": "Valid parameters found",
                    "data": {
                        "attempt": attempt + 1,
                        "n_components": n_components,
                        "signal_types": signal_types
                    },
                    "timestamp": int(time.time() * 1000)
                }
                with open(log_path_local, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception:
                pass
            # #endregion
            return xs, IFs, signal_types
        logger.debug(
            f"Attempt {attempt + 1} failed. IFs: "
            f"{[f'[{IF.min():.2f}, {IF.max():.2f}]' for IF in IFs]}"
        )
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "R",
            "location": "sample_generator.py:draw_valid_params_for_components:FAILED",
            "message": "Failed to find valid parameters",
            "data": {
                "max_tries": max_tries,
                "n_components": n_components,
                "fmax": fmax,
                "signal_scenario": signal_scenario
            },
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path_local, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    raise SignalGenerationError(
        f"Could not find valid parameters within {max_tries} attempts."
    )


def generate_sample(
    rng: np.random.Generator,
    config: SyntheticDataConfig,
    n_components: int,
    snr_db: float,
    tf_sigma: Optional[float] = None,
    signal_scenario: Optional[str] = None,
    freq_range: Optional[Tuple[float, float]] = None
) -> Sample:
    """
    Generate a complete synthetic sample with all required data.
    
    Why: Provides a single entry point for sample generation, orchestrating
    all steps from parameter generation to TF representation creation.
    This ensures consistent sample creation across the codebase.
    
    What: Generates valid component signals, sums them to create a clean signal,
    adds noise, computes STFT, generates ideal TF representation, and creates
    a binary mask. Returns a complete Sample object with all data.
    
    Args:
        rng: NumPy random number generator.
        config: SyntheticDataConfig object with all configuration parameters.
        n_components: Number of signal components (1-8).
        snr_db: Signal-to-noise ratio in dB.
        tf_sigma: Gaussian blur sigma for TF representation. If None, uses
            a random value from config.tf_sigma_range. Default None.
        signal_scenario: Optional signal scenario name. If provided, generates
            only that signal type. Default None.
        freq_range: Optional frequency range tuple (fmin, fmax). If provided,
            uses range-specific n_freq_bins, nfft, and fmax. Default None.
    
    Returns:
        Sample: Complete sample object with all required data.
    
    Raises:
        SignalGenerationError: If valid parameters cannot be generated.
        ValueError: If any parameter is invalid.
    """
    t = np.arange(config.n_samples) / config.fs
    
    if freq_range:
        fmax = freq_range[1]
        n_freq_bins = config.get_n_freq_bins_for_range(fmax)
        nfft = config.get_nfft_for_range(fmax)
    else:
        fmax = config.fmax
        n_freq_bins = config.n_freq_bins
        nfft = config.nfft
    
    xs, IFs, signal_types_list = draw_valid_params_for_components(
        rng, n_components, t, fmax, signal_scenario=signal_scenario
    )
    x_clean = np.sum(np.stack(xs, axis=0), axis=0)
    x_noisy = awgn(x_clean, snr_db=snr_db, rng=rng)
    S = stft_mag_128x8000(
        x_noisy,
        config.n_samples,
        nfft=nfft,
        win_len=config.win_len,
        hop=config.hop
    )
    
    if tf_sigma is None:
        tf_sigma = rng.uniform(
            config.tf_sigma_range[0],
            config.tf_sigma_range[1]
        )
    
    tf_ideal = ifs_to_ideal_tf(
        IFs,
        n_freq_bins=n_freq_bins,
        n_time_bins=config.n_time_bins,
        fmax=fmax,
        sigma_bins=tf_sigma
    )
    ifs_norm = (np.stack(IFs, axis=0) / fmax).astype(np.float32)
    binary_mask = generate_binary_mask(tf_ideal)
    
    return Sample(
        n_components=n_components,
        x_clean=x_clean.astype(np.float32),
        x_noisy=x_noisy.astype(np.float32),
        stft=S,
        ifs_hz=IFs,
        ifs_norm=ifs_norm,
        tf_ideal=tf_ideal,
        binary_mask=binary_mask,
        signal_types=signal_types_list
    )
