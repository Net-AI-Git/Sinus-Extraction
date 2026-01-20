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
from .signal_models import (
    PolyPhaseParams,
    CosChirpParams,
    StepSineParams,
    gen_poly_params,
    gen_coschirp_params,
    gen_step_sine_params
)
from .signal_generators import (
    poly_signal_and_if,
    coschirp_signal_and_if,
    step_sine_signal_and_if
)
from .signal_processing import awgn, hanning, stft_mag_128x8000
from .tf_representation import ifs_to_ideal_tf, generate_binary_mask
from .visualization import (
    save_image,
    generate_and_display_pairs,
    generate_and_display_pairs_convenience
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
    'gen_poly_params',
    'gen_coschirp_params',
    'gen_step_sine_params',
    'poly_signal_and_if',
    'coschirp_signal_and_if',
    'step_sine_signal_and_if',
    'awgn',
    'hanning',
    'stft_mag_128x8000',
    'ifs_to_ideal_tf',
    'generate_binary_mask',
    'save_image',
    'generate_and_display_pairs',
    'generate_and_display_pairs_convenience',
    'SyntheticDataError',
    'InvalidParameterError',
    'SignalGenerationError',
    'ConfigurationError',
]
