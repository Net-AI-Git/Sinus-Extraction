"""
Synthetic Data Generation Package.

This package provides tools for generating synthetic sine wave signals with
various modulation types, computing their time-frequency representations,
and creating training datasets for segmentation models.

Why: Packaging the synthetic data generation functionality allows easy
import and reuse across the project. The package structure follows project
standards with clear separation of concerns.

What: Provides modules for configuration, signal models, signal processing,
signal generation, time-frequency representation, sample generation, and
visualization. The main entry point is main.py for batch generation.
"""

from .config import SyntheticDataConfig
from .sample_generator import Sample, generate_sample
from .main import (
    generate_samples_by_scenario,
    generate_all_scenarios,
    generate_diverse_samples
)
from .signal_models import (
    PolyPhaseParams,
    CosChirpParams,
    StepSineParams,
    FreqJumpParams,
    SawtoothModParams,
    SquareModParams,
    PhaseJumpParams,
    AmplitudeModParams,
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
from .signal_processing import awgn, hanning, stft_mag_128x8000
from .tf_representation import ifs_to_ideal_tf, generate_binary_mask
from .visualization import (
    save_image,
    save_array,
    generate_and_display_pairs,
    generate_and_display_pairs_convenience
)
from .utils import (
    scan_directory_for_samples,
    validate_array_file,
    list_samples_in_scenario,
    extract_uuid_from_filename
)
from .exceptions import (
    SyntheticDataError,
    InvalidParameterError,
    SignalGenerationError,
    ConfigurationError
)

__all__ = [
    'SyntheticDataConfig',
    'Sample',
    'generate_sample',
    'PolyPhaseParams',
    'CosChirpParams',
    'StepSineParams',
    'FreqJumpParams',
    'SawtoothModParams',
    'SquareModParams',
    'PhaseJumpParams',
    'AmplitudeModParams',
    'gen_poly_params',
    'gen_coschirp_params',
    'gen_step_sine_params',
    'gen_freq_jump_params',
    'gen_sawtooth_mod_params',
    'gen_square_mod_params',
    'gen_phase_jump_params',
    'gen_amplitude_mod_params',
    'poly_signal_and_if',
    'coschirp_signal_and_if',
    'step_sine_signal_and_if',
    'freq_jump_signal_and_if',
    'sawtooth_mod_signal_and_if',
    'square_mod_signal_and_if',
    'phase_jump_signal_and_if',
    'amplitude_mod_signal_and_if',
    'awgn',
    'hanning',
    'stft_mag_128x8000',
    'ifs_to_ideal_tf',
    'generate_binary_mask',
    'save_image',
    'save_array',
    'generate_and_display_pairs',
    'generate_and_display_pairs_convenience',
    'scan_directory_for_samples',
    'validate_array_file',
    'list_samples_in_scenario',
    'extract_uuid_from_filename',
    'generate_samples_by_scenario',
    'generate_all_scenarios',
    'generate_diverse_samples',
    'SyntheticDataError',
    'InvalidParameterError',
    'SignalGenerationError',
    'ConfigurationError',
]
