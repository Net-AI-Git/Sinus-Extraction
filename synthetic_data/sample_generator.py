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
    gen_step_sine_params
)
from .signal_generators import (
    poly_signal_and_if,
    coschirp_signal_and_if,
    step_sine_signal_and_if
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


def _generate_component_signals(
    rng: np.random.Generator,
    n_components: int,
    t: np.ndarray
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Generate signals and IFs for each component type.
    
    Why: Separates the component generation logic for clarity and testability.
    This function handles the conditional logic for generating different numbers
    of components with different signal types.
    
    What: Generates signals based on n_components:
    - 1-2 components: polynomial phase signals
    - 3 components: 2 polynomial + 1 cosine chirp
    - 4 components: 2 polynomial + 1 cosine chirp + 1 step sine
    Returns lists of signal arrays and IF arrays.
    
    Args:
        rng: NumPy random number generator.
        n_components: Number of components to generate (1-4).
        t: Time vector in seconds.
    
    Returns:
        Tuple[List[np.ndarray], List[np.ndarray]]: A tuple containing:
            - List of signal arrays, one per component.
            - List of IF arrays in Hz, one per component.
    
    Raises:
        ValueError: If n_components is not in [1, 4].
    """
    if not 1 <= n_components <= 4:
        raise ValueError(
            f"Number of components must be in [1, 4], got {n_components}."
        )
    
    xs, IFs = [], []
    if n_components >= 1:
        p1 = gen_poly_params(rng)
        x1, IF1 = poly_signal_and_if(t, p1)
        xs.append(x1)
        IFs.append(IF1)
    if n_components >= 2:
        p2 = gen_poly_params(rng)
        x2, IF2 = poly_signal_and_if(t, p2)
        xs.append(x2)
        IFs.append(IF2)
    if n_components >= 3:
        q = gen_coschirp_params(rng)
        x3, IF3 = coschirp_signal_and_if(t, q)
        xs.append(x3)
        IFs.append(IF3)
    if n_components == 4:
        step_params = gen_step_sine_params(rng)
        x4, IF4 = step_sine_signal_and_if(t, step_params)
        xs.append(x4)
        IFs.append(IF4)
    
    return xs, IFs


def draw_valid_params_for_components(
    rng: np.random.Generator,
    n_components: int,
    t: np.ndarray,
    fmax: float,
    max_tries: int = 200
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
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
        n_components: Number of components to generate (1-4).
        t: Time vector in seconds.
        fmax: Maximum frequency (Nyquist) in Hz.
        max_tries: Maximum number of attempts to find valid parameters.
            Default 200.
    
    Returns:
        Tuple[List[np.ndarray], List[np.ndarray]]: A tuple containing:
            - List of signal arrays, one per component.
            - List of IF arrays in Hz, one per component.
    
    Raises:
        SignalGenerationError: If valid parameters cannot be found within
            max_tries attempts.
    """
    for attempt in range(max_tries):
        xs, IFs = _generate_component_signals(rng, n_components, t)
        if params_valid(IFs, fmin=0.0, fmax=fmax):
            return xs, IFs
        logger.debug(
            f"Attempt {attempt + 1} failed. IFs: "
            f"{[f'[{IF.min():.2f}, {IF.max():.2f}]' for IF in IFs]}"
        )
    
    raise SignalGenerationError(
        f"Could not find valid parameters within {max_tries} attempts."
    )


def generate_sample(
    rng: np.random.Generator,
    config: SyntheticDataConfig,
    n_components: int,
    snr_db: float,
    tf_sigma: Optional[float] = None
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
        n_components: Number of signal components (1-4).
        snr_db: Signal-to-noise ratio in dB.
        tf_sigma: Gaussian blur sigma for TF representation. If None, uses
            a random value from config.tf_sigma_range. Default None.
    
    Returns:
        Sample: Complete sample object with all required data.
    
    Raises:
        SignalGenerationError: If valid parameters cannot be generated.
        ValueError: If any parameter is invalid.
    """
    t = np.arange(config.n_samples) / config.fs
    xs, IFs = draw_valid_params_for_components(
        rng, n_components, t, config.fmax
    )
    x_clean = np.sum(np.stack(xs, axis=0), axis=0)
    x_noisy = awgn(x_clean, snr_db=snr_db, rng=rng)
    S = stft_mag_128x8000(
        x_noisy,
        config.n_samples,
        nfft=config.nfft,
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
        n_freq_bins=config.n_freq_bins,
        n_time_bins=config.n_time_bins,
        fmax=config.fmax,
        sigma_bins=tf_sigma
    )
    ifs_norm = (np.stack(IFs, axis=0) / config.fmax).astype(np.float32)
    binary_mask = generate_binary_mask(tf_ideal)
    
    return Sample(
        n_components=n_components,
        x_clean=x_clean.astype(np.float32),
        x_noisy=x_noisy.astype(np.float32),
        stft=S,
        ifs_hz=IFs,
        ifs_norm=ifs_norm,
        tf_ideal=tf_ideal,
        binary_mask=binary_mask
    )
