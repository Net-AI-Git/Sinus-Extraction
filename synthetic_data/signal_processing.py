"""
Signal processing utilities for synthetic data generation.

This module provides functions for signal processing operations including
noise addition, window functions, and Short-Time Fourier Transform (STFT)
computation.

Why: Centralizing signal processing utilities ensures consistent implementation
across the codebase and allows reuse of common operations. Separating these
functions from signal generation logic improves modularity and testability.

What: Provides functions for adding white Gaussian noise, generating Hanning
windows, and computing STFT magnitude spectrograms. All functions are designed
to work with configurable parameters rather than global constants.
"""

from typing import Tuple
import numpy as np


def awgn(
    x: np.ndarray,
    snr_db: float,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Add white Gaussian noise to a signal to achieve a target SNR.
    
    Why: Noise addition is essential for creating realistic synthetic data
    with varying signal-to-noise ratios. This function ensures the noise
    power is correctly scaled to achieve the desired SNR in dB.
    
    What: Computes the signal power, calculates the required noise power
    based on the target SNR, generates Gaussian noise with the appropriate
    variance, and adds it to the input signal.
    
    Args:
        x: Input signal array. Must be a 1D numpy array.
        snr_db: Target signal-to-noise ratio in decibels. Can be negative
            (noise stronger than signal) or positive (signal stronger than noise).
        rng: NumPy random number generator for reproducible noise generation.
    
    Returns:
        np.ndarray: Signal with added noise, same shape as input.
    
    Raises:
        ValueError: If input signal is empty or has zero power.
    """
    p_sig = np.mean(np.abs(x) ** 2)
    snr_lin = 10 ** (snr_db / 10.0)
    p_noise = p_sig / snr_lin
    noise = rng.normal(0.0, np.sqrt(p_noise), size=x.shape)
    return x + noise


def hanning(M: int) -> np.ndarray:
    """
    Generate a continuous-discrete Hanning window of length M.
    
    Why: Hanning windows are commonly used in STFT computation to reduce
    spectral leakage. This function provides a standard implementation
    that matches the expected window shape.
    
    What: Generates a Hanning window using the formula:
    0.5 - 0.5 * cos(2π * n / (M - 1)) for n = 0, 1, ..., M-1.
    
    Args:
        M: Window length in samples. Must be positive.
    
    Returns:
        np.ndarray: Hanning window of length M, values in [0, 1].
    
    Raises:
        ValueError: If M <= 0.
    """
    if M <= 0:
        raise ValueError(f"Window length must be positive, got {M}.")
    n = np.arange(M)
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * n / (M - 1))


def _compute_stft_frames(
    x_pad: np.ndarray,
    signal_length: int,
    win_len: int,
    hop: int,
    nfft: int
) -> np.ndarray:
    """
    Compute STFT frames from a padded signal.
    
    Why: Separates the frame computation logic from normalization, allowing
    for better modularity and testing. This function handles the core STFT
    computation including windowing and FFT.
    
    What: Iterates over the signal with the specified hop size, extracts
    windowed segments, applies FFT, and stacks the magnitude spectra into
    a 2D array.
    
    Args:
        x_pad: Padded input signal array.
        signal_length: Original signal length (before padding).
        win_len: Window length in samples.
        hop: Hop size in samples.
        nfft: FFT size.
    
    Returns:
        np.ndarray: STFT magnitude frames, shape [nfft//2 + 1, n_frames].
    """
    w = hanning(win_len)
    frames = []
    for t in range(0, signal_length, hop):
        seg = x_pad[t: t + win_len]
        if len(seg) < win_len:
            seg = np.pad(seg, (0, win_len - len(seg)))
        X = np.fft.rfft(seg * w, n=nfft)
        frames.append(np.abs(X))
    return np.stack(frames, axis=1)


def _normalize_spectrogram(S: np.ndarray) -> np.ndarray:
    """
    Normalize spectrogram to [0, 1] range.
    
    Why: Normalization ensures consistent scaling across different signals
    and prevents numerical issues. This function provides stable normalization
    that handles edge cases (zero or very small maximum values).
    
    What: Divides the spectrogram by its maximum value (plus a small epsilon
    to prevent division by zero) and converts to float32 for memory efficiency.
    
    Args:
        S: Input spectrogram array, any shape.
    
    Returns:
        np.ndarray: Normalized spectrogram in [0, 1] range, float32 dtype.
    """
    S = S / (np.max(S) + 1e-12)
    return S.astype(np.float32)


def stft_mag_128x8000(
    x: np.ndarray,
    signal_length: int,
    nfft: int = 4000,
    win_len: int = 57,
    hop: int = 1
) -> np.ndarray:
    """
    Compute STFT magnitude spectrogram with Hanning window.
    
    Why: STFT is the core signal processing operation for time-frequency
    analysis. This function provides a complete STFT implementation with
    proper windowing, padding, and normalization for consistent results.
    
    What: Pads the input signal with reflection to handle edge effects,
    computes STFT frames using a Hanning window, removes the Nyquist
    frequency bin, and normalizes the result to [0, 1] range. Returns a
    spectrogram of dimensions [n_freq_bins, n_time_bins].
    
    Args:
        x: Input signal array. Must be 1D with length equal to signal_length.
        signal_length: Expected signal length. Used for validation and
            frame computation.
        nfft: FFT size. Default 4000.
        win_len: Window length in samples. Default 57.
        hop: Hop size in samples. Default 1 for maximum time resolution.
    
    Returns:
        np.ndarray: STFT magnitude spectrogram, shape [n_freq_bins, n_time_bins],
            normalized to [0, 1], dtype float32. n_freq_bins = nfft // 2,
            n_time_bins = signal_length.
    
    Raises:
        ValueError: If signal length doesn't match expected length or if
            any parameter is invalid.
    """
    if len(x) != signal_length:
        raise ValueError(
            f"Signal length must be {signal_length}, got {len(x)}."
        )
    pad = win_len // 2
    x_pad = np.pad(x, (pad, pad), mode='reflect')
    S = _compute_stft_frames(x_pad, signal_length, win_len, hop, nfft)
    S = S[:-1, :]  # Remove Nyquist frequency
    return _normalize_spectrogram(S)
