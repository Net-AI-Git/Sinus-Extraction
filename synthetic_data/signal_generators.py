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

from .signal_models import (
    PolyPhaseParams,
    CosChirpParams,
    StepSineParams,
    FreqJumpParams,
    SawtoothModParams,
    SquareModParams,
    PhaseJumpParams,
    AmplitudeModParams
)


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


def freq_jump_signal_and_if(
    t: np.ndarray,
    params: FreqJumpParams,
    amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate frequency jump signal and its instantaneous frequency.
    
    Why: Frequency jump signals create sharp "dancing" patterns in
    time-frequency representations. This function implements signals with
    sudden frequency changes that create visually striking patterns.
    
    What: Generates a signal with piecewise constant frequencies that
    jump instantly at specified times. The phase is continuous (integrated
    from IF), and the IF jumps between frequencies at jump_times.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: FreqJumpParams object containing jump times and frequencies.
        amplitude: Signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    x = np.zeros_like(t)
    IF = np.zeros_like(t)
    start = 0
    
    for i in range(params.n_jumps):
        end = np.searchsorted(t, params.jump_times[i])
        freq = params.freqs[i]
        IF[start:end] = freq
        phase = 2 * np.pi * freq * (t[start:end] - t[start])
        if start > 0:
            phase += 2 * np.pi * params.freqs[i-1] * (t[start] - t[0])
        x[start:end] = amplitude * np.sin(phase)
        start = end
    
    if start < len(t):
        freq = params.freqs[-1]
        IF[start:] = freq
        phase = 2 * np.pi * freq * (t[start:] - t[start])
        if start > 0:
            phase += 2 * np.pi * params.freqs[-2] * (t[start] - t[0])
        x[start:] = amplitude * np.sin(phase)
    
    return x, IF


def sawtooth_mod_signal_and_if(
    t: np.ndarray,
    params: SawtoothModParams,
    amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate sawtooth modulation signal and its instantaneous frequency.
    
    Why: Sawtooth modulation creates linearly varying frequency patterns
    that create sharp "dancing" visual effects in time-frequency representations.
    
    What: Generates a signal with sawtooth frequency modulation. The IF
    varies linearly in a sawtooth pattern, and the phase is integrated
    from the IF to ensure continuity.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: SawtoothModParams object containing modulation parameters.
        amplitude: Signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    sawtooth = 2 * (t * params.mod_freq - np.floor(t * params.mod_freq + 0.5))
    IF = params.base_freq + params.mod_depth * params.base_freq * sawtooth
    dt = t[1] - t[0] if len(t) > 1 else 0.0
    phase = 2 * np.pi * np.cumsum(IF) * dt
    if len(t) > 1:
        phase = np.concatenate([[0.0], phase[:-1]])
    x = amplitude * np.sin(phase)
    return x, IF


def square_mod_signal_and_if(
    t: np.ndarray,
    params: SquareModParams,
    amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate square wave modulation signal and its instantaneous frequency.
    
    Why: Square wave modulation creates abrupt frequency changes that
    create sharp "dancing" patterns in time-frequency representations.
    
    What: Generates a signal with square wave frequency modulation. The IF
    switches between two values based on a square wave pattern, and the
    phase is integrated from the IF to ensure continuity.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: SquareModParams object containing modulation parameters.
        amplitude: Signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    period = 1.0 / params.mod_freq
    phase_mod = (t % period) / period
    square = np.where(phase_mod < params.duty_cycle, 1.0, -1.0)
    IF = params.base_freq + params.mod_depth * params.base_freq * square
    dt = t[1] - t[0] if len(t) > 1 else 0.0
    phase = 2 * np.pi * np.cumsum(IF) * dt
    if len(t) > 1:
        phase = np.concatenate([[0.0], phase[:-1]])
    x = amplitude * np.sin(phase)
    return x, IF


def phase_jump_signal_and_if(
    t: np.ndarray,
    params: PhaseJumpParams,
    amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate phase jump signal and its instantaneous frequency.
    
    Why: Phase jump signals create sudden phase discontinuities that
    create sharp transitions in time-frequency representations, creating
    "dancing" visual effects.
    
    What: Generates a signal with constant frequency but sudden phase
    jumps at specified times. The IF remains constant, but the phase
    accumulates jumps.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: PhaseJumpParams object containing jump parameters.
        amplitude: Signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    IF = np.full_like(t, params.base_freq)
    phase = 2 * np.pi * params.base_freq * t
    
    for i, jump_time in enumerate(params.jump_times):
        idx = np.searchsorted(t, jump_time)
        if idx < len(t):
            phase[idx:] += params.jump_sizes[i]
    
    x = amplitude * np.sin(phase)
    return x, IF


def amplitude_mod_signal_and_if(
    t: np.ndarray,
    params: AmplitudeModParams,
    base_amplitude: float = 5000.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate amplitude modulation signal and its instantaneous frequency.
    
    Why: Amplitude modulation creates time-varying amplitude patterns that
    create dynamic "dancing" visual effects in time-frequency representations.
    
    What: Generates a signal with amplitude modulation. The amplitude
    varies sinusoidally, while the frequency remains constant. The IF
    is constant at base_freq.
    
    Args:
        t: Time vector in seconds. Must be 1D numpy array.
        params: AmplitudeModParams object containing modulation parameters.
        base_amplitude: Base signal amplitude. Default 5000.0.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing:
            - Signal array x(t), same shape as t.
            - Instantaneous frequency array IF(t) in Hz, same shape as t.
    """
    amplitude = base_amplitude * (1.0 + params.mod_depth * np.cos(2 * np.pi * params.mod_freq * t))
    phase = 2 * np.pi * params.base_freq * t
    x = amplitude * np.sin(phase)
    IF = np.full_like(t, params.base_freq)
    return x, IF
