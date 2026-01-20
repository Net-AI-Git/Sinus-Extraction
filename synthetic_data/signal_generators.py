"""
Signal generation functions for synthetic data.

This module provides functions to generate signals with various modulation
types and compute their instantaneous frequency (IF) trajectories.

Why: Separating signal generation from parameter models improves modularity
and allows independent testing. These functions implement the mathematical
models for different signal types with time-varying instantaneous frequency.

What: Provides functions to generate polynomial phase signals, cosine chirp
signals, and step sine signals, along with their corresponding instantaneous
frequency trajectories. All functions return both the signal and its IF.
"""

from typing import Tuple, List
import numpy as np

from .signal_models import PolyPhaseParams, CosChirpParams, StepSineParams


def poly_signal_and_if(
    t: np.ndarray,
    p: PolyPhaseParams,
    amplitude: float = 5000.0,
    kl: float = 100.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate polynomial phase signal and its instantaneous frequency.
    
    Why: Polynomial phase signals provide a flexible model for signals with
    time-varying frequency. This function implements the mathematical model
    and computes both the signal and its IF for use in time-frequency analysis.
    
    What: Generates a signal using the formula:
    x(t) = amplitude * cos(kl * 2π * [a + bt + ct² + dt³ + et⁴ + ht⁵])
    and computes the IF as the derivative of the phase:
    IF(t) = kl * (b + 2ct + 3dt² + 4et³ + 5ht⁴)
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        p: PolyPhaseParams object containing polynomial coefficients.
        amplitude: Signal amplitude. Default 5000.0.
        kl: Frequency scaling factor. Default 100.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    phase = 2 * np.pi * (
        p.a + p.b * t + p.c * t**2 + p.d * t**3 + p.e * t**4 + p.h * t**5
    )
    x = amplitude * np.cos(kl * phase)
    IF = kl * (
        p.b + 2 * p.c * t + 3 * p.d * t**2 + 4 * p.e * t**3 + 5 * p.h * t**4
    )
    return x, IF


def coschirp_signal_and_if(
    t: np.ndarray,
    q: CosChirpParams,
    amplitude: float = 1000.0,
    Ks: float = 5.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate cosine chirp signal and its instantaneous frequency.
    
    Why: Cosine chirp signals provide a model for frequency-modulated signals
    with sinusoidal frequency variation. This function implements the mathematical
    model and computes both the signal and its IF.
    
    What: Generates a signal using the formula:
    x(t) = amplitude * sin(Ks * 2π * [aπ cos(bπt + π) + ct])
    and computes the IF as the derivative of the phase:
    IF(t) = Ks * (c - a*b*π² * sin(bπt + π))
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        q: CosChirpParams object containing cosine chirp parameters.
        amplitude: Signal amplitude. Default 1000.0.
        Ks: Frequency scaling factor. Default 5.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    phase_inner = (
        q.a * np.pi * np.cos(q.b * np.pi * t + np.pi) + q.c * t
    )
    x = amplitude * np.sin(Ks * 2 * np.pi * phase_inner)
    IF = Ks * (
        q.c - (q.a * q.b * (np.pi**2)) * np.sin(q.b * np.pi * t + np.pi)
    )
    return x, IF


def _compute_chirp_phase(
    t_segment: np.ndarray,
    freq_start: float,
    freq_end: float
) -> np.ndarray:
    """
    Compute phase for a linear chirp segment.
    
    Why: Separates the chirp phase computation logic for reusability and
    clarity. This function handles the mathematical computation of phase
    for a linear frequency sweep.
    
    What: Computes the phase for a linear chirp using the formula:
    phase(t) = 2π * (f_start * t + 0.5 * (f_end - f_start) * t² / T)
    where T is the duration of the segment.
    
    Args:
        t_segment: Time vector for the segment.
        freq_start: Starting frequency in Hz.
        freq_end: Ending frequency in Hz.
    
    Returns:
        np.ndarray: Phase array for the chirp segment.
    """
    if len(t_segment) == 0:
        return np.array([])
    T = t_segment[-1] - t_segment[0]
    if T == 0:
        return 2 * np.pi * freq_start * t_segment
    phase = 2 * np.pi * (
        freq_start * t_segment +
        0.5 * (freq_end - freq_start) * t_segment**2 / T
    )
    return phase


def step_sine_signal_and_if(
    t: np.ndarray,
    params: StepSineParams,
    amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate step sine signal with smooth frequency transitions.
    
    Why: Step sine signals with smooth transitions provide a realistic model
    for signals with piecewise constant frequencies. Linear chirps between
    steps ensure continuous phase and avoid discontinuities.
    
    What: Generates a signal with piecewise constant frequencies connected by
    linear chirps. For each step, computes the IF as a linear interpolation
    between frequencies, and the phase using a linear chirp formula. The
    final segment uses constant frequency.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: StepSineParams object containing frequency steps and step times.
        amplitude: Signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    x = np.zeros_like(t)
    IF = np.zeros_like(t)
    start = 0
    
    for i in range(len(params.step_times)):
        end = np.searchsorted(t, params.step_times[i])
        freq_start = params.freq_steps[i]
        freq_end = params.freq_steps[i + 1]
        IF[start:end] = np.linspace(freq_start, freq_end, end - start)
        t_segment = t[start:end]
        phase = _compute_chirp_phase(t_segment, freq_start, freq_end)
        x[start:end] = amplitude * np.sin(phase)
        start = end
    
    if start < len(t):
        freq = params.freq_steps[-1]
        t_segment = t[start:]
        phase = 2 * np.pi * freq * t_segment
        x[start:] = amplitude * np.sin(phase)
        IF[start:] = freq
    
    return x, IF
