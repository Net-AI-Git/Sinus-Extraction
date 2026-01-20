"""
Configuration module for Synthetic Data Generation.

This module provides a type-safe configuration class using pydantic-settings
for the synthetic data generation pipeline, including signal parameters,
processing settings, and output paths.

Why: Centralized configuration management ensures consistency across the codebase,
enables easy experimentation with different parameters, and provides type
safety and validation to catch configuration errors early. Using pydantic-settings
allows environment variable overrides and validation.

What: Defines a SyntheticDataConfig class that encapsulates all configuration
parameters for synthetic data generation, including sampling rate, duration,
SNR levels, STFT parameters, and output directories. Includes validation logic
to ensure all values are within acceptable ranges.
"""

from typing import List, Tuple
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from .exceptions import ConfigurationError


class SyntheticDataConfig(BaseSettings):
    """
    Type-safe configuration container for synthetic data generation.
    
    Why: Using pydantic-settings provides type safety, validation, and clear
    documentation of all configuration parameters. This prevents runtime errors
    from typos or invalid values and makes the configuration self-documenting.
    The configuration supports environment variable overrides via .env files.
    
    What: A pydantic BaseSettings class that encapsulates all hyperparameters
    and settings for the synthetic data generation pipeline. Configured for
    generating synthetic sine wave signals with various modulation types and
    noise levels. The configuration includes validation logic to ensure all
    values are within acceptable ranges.
    
    Attributes:
        fs: Sampling rate in Hz. Default 4000 Hz provides sufficient frequency
            resolution for signals up to 2000 Hz (Nyquist frequency).
        duration: Signal duration in seconds. Default 2.0 seconds provides
            sufficient time resolution for time-frequency analysis.
        n_samples: Number of samples per signal. Computed as fs * duration.
        fmax: Maximum frequency (Nyquist frequency). Computed as fs / 2.0.
        snr_list: List of SNR levels in dB for noise addition. Default values
            range from -5 dB (very noisy) to 35 dB (very clean).
        nfft: FFT size for STFT computation. Default 4000 matches the sampling
            rate for optimal frequency resolution.
        win_len: Window length for STFT. Default 57 samples provides good
            time-frequency trade-off.
        hop: Hop size for STFT. Default 1 provides maximum time resolution.
        n_freq_bins: Number of frequency bins in output spectrogram. Default
            2000 matches the number of positive frequency bins from FFT.
        n_time_bins: Number of time bins in output spectrogram. Default 8000
            matches the number of samples.
        tf_sigma_range: Range for Gaussian blur sigma in TF representation.
            Tuple of (min, max) values. Default (0.5, 2.0) provides reasonable
            blur for ideal TF mask generation.
        output_dir: Output directory for generated samples. Default './data'.
        seed: Random seed for reproducibility. Default 42.
    """
    
    # Signal Configuration
    fs: float = Field(
        default=4000.0,
        description="Sampling rate in Hz"
    )
    duration: float = Field(
        default=2.0,
        description="Signal duration in seconds"
    )
    
    # SNR Configuration
    snr_list: List[float] = Field(
        default=[-5, 1, 2, 1, 1, 5, 10, 15, 20, 25, 30, 35],
        description="List of SNR levels in dB for noise addition"
    )
    
    # STFT Configuration
    nfft: int = Field(
        default=4000,
        description="FFT size for STFT computation"
    )
    win_len: int = Field(
        default=57,
        description="Window length for STFT in samples"
    )
    hop: int = Field(
        default=1,
        description="Hop size for STFT in samples"
    )
    
    # Output Configuration
    n_freq_bins: int = Field(
        default=2000,
        description="Number of frequency bins in output spectrogram"
    )
    n_time_bins: int = Field(
        default=8000,
        description="Number of time bins in output spectrogram"
    )
    tf_sigma_range: Tuple[float, float] = Field(
        default=(0.5, 2.0),
        description="Range for Gaussian blur sigma in TF representation (min, max)"
    )
    output_dir: str = Field(
        default='./data',
        description="Output directory for generated samples"
    )
    
    # Random Seed
    seed: int = Field(
        default=42,
        description="Random seed for reproducibility"
    )
    
    @field_validator('fs')
    @classmethod
    def validate_fs(cls, v: float) -> float:
        """Validate sampling rate is positive."""
        if v <= 0:
            raise ConfigurationError(f"Sampling rate must be positive, got {v}.")
        return v
    
    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v: float) -> float:
        """Validate duration is positive."""
        if v <= 0:
            raise ConfigurationError(f"Duration must be positive, got {v}.")
        return v
    
    @field_validator('nfft')
    @classmethod
    def validate_nfft(cls, v: int) -> int:
        """Validate FFT size is positive and power of 2."""
        if v <= 0:
            raise ConfigurationError(f"FFT size must be positive, got {v}.")
        return v
    
    @field_validator('win_len')
    @classmethod
    def validate_win_len(cls, v: int) -> int:
        """Validate window length is positive."""
        if v <= 0:
            raise ConfigurationError(f"Window length must be positive, got {v}.")
        return v
    
    @field_validator('hop')
    @classmethod
    def validate_hop(cls, v: int) -> int:
        """Validate hop size is positive."""
        if v <= 0:
            raise ConfigurationError(f"Hop size must be positive, got {v}.")
        return v
    
    @field_validator('n_freq_bins')
    @classmethod
    def validate_n_freq_bins(cls, v: int) -> int:
        """Validate number of frequency bins is positive."""
        if v <= 0:
            raise ConfigurationError(f"Number of frequency bins must be positive, got {v}.")
        return v
    
    @field_validator('n_time_bins')
    @classmethod
    def validate_n_time_bins(cls, v: int) -> int:
        """Validate number of time bins is positive."""
        if v <= 0:
            raise ConfigurationError(f"Number of time bins must be positive, got {v}.")
        return v
    
    @field_validator('tf_sigma_range')
    @classmethod
    def validate_tf_sigma_range(cls, v: Tuple[float, float]) -> Tuple[float, float]:
        """Validate TF sigma range is valid."""
        min_val, max_val = v
        if min_val <= 0 or max_val <= 0:
            raise ConfigurationError(
                f"TF sigma range values must be positive, got {v}."
            )
        if min_val >= max_val:
            raise ConfigurationError(
                f"TF sigma min must be less than max, got {v}."
            )
        return v
    
    @field_validator('seed')
    @classmethod
    def validate_seed(cls, v: int) -> int:
        """Validate seed is non-negative."""
        if v < 0:
            raise ConfigurationError(f"Seed must be non-negative, got {v}.")
        return v
    
    @property
    def n_samples(self) -> int:
        """
        Compute number of samples from sampling rate and duration.
        
        Why: Provides a convenient property to compute the number of samples
        without storing it as a separate field, ensuring it's always consistent
        with fs and duration.
        
        What: Computes n_samples as int(fs * duration), rounding to the nearest
        integer to ensure an integer number of samples.
        
        Returns:
            int: Number of samples in the signal.
        """
        return int(self.fs * self.duration)
    
    @property
    def fmax(self) -> float:
        """
        Compute maximum frequency (Nyquist frequency).
        
        Why: Provides a convenient property to compute the Nyquist frequency
        without storing it as a separate field, ensuring it's always consistent
        with the sampling rate.
        
        What: Computes fmax as fs / 2.0, which is the Nyquist frequency that
        determines the maximum representable frequency in the signal.
        
        Returns:
            float: Maximum frequency (Nyquist frequency) in Hz.
        """
        return self.fs / 2.0
    
    class Config:
        """Pydantic configuration."""
        env_prefix = 'SYNTHETIC_DATA_'
        case_sensitive = False
