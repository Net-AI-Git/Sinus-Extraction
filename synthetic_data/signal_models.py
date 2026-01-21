"""
Signal model parameter classes and generation.

This module defines Pydantic models for signal parameters and functions
to generate random parameters for different signal types.

Why: Using Pydantic models provides type safety, validation, and clear
documentation of signal parameters. This ensures parameters are always
valid and makes the code self-documenting. Parameter generation functions
encapsulate the logic for sampling valid parameter ranges.

What: Defines parameter classes for polynomial phase signals and cosine
chirp signals, along with functions to generate random parameters within
valid ranges. Also provides a helper function for uniform parameter sampling.
"""

from typing import List, Optional
import numpy as np
from pydantic import BaseModel, Field


class PolyPhaseParams(BaseModel):
    """
    Parameters for polynomial phase signal generation.
    
    Why: Encapsulates the six polynomial coefficients needed to generate
    a polynomial phase signal. Using a Pydantic model ensures type safety
    and allows validation of parameter ranges.
    
    What: A Pydantic BaseModel containing six float parameters (a, b, c, d, e, h)
    that define a 5th-order polynomial phase function. These parameters are
    used to generate signals with time-varying instantaneous frequency.
    
    Attributes:
        a: Constant phase term. Range typically [-5.0, 5.0].
        b: Linear phase coefficient. Range typically [0.0, 10.0].
        c: Quadratic phase coefficient. Range typically [-2.0, 2.0].
        d: Cubic phase coefficient. Range typically [-1.0, 1.0].
        e: Quartic phase coefficient. Range typically [-0.5, 0.5].
        h: Quintic phase coefficient. Range typically [-0.2, 0.2].
    """
    a: float = Field(description="Constant phase term")
    b: float = Field(description="Linear phase coefficient")
    c: float = Field(description="Quadratic phase coefficient")
    d: float = Field(description="Cubic phase coefficient")
    e: float = Field(description="Quartic phase coefficient")
    h: float = Field(description="Quintic phase coefficient")


class CosChirpParams(BaseModel):
    """
    Parameters for cosine chirp signal generation.
    
    Why: Encapsulates the three parameters needed to generate a cosine
    chirp signal. Using a Pydantic model ensures type safety and allows
    validation of parameter ranges.
    
    What: A Pydantic BaseModel containing three float parameters (a, b, c)
    that define a cosine-modulated chirp signal. Parameter 'a' controls
    the amplitude of the cosine modulation, 'b' controls the frequency
    of the cosine, and 'c' controls the linear chirp rate.
    
    Attributes:
        a: Cosine modulation amplitude. Range typically [0.0, 1.0].
        b: Cosine modulation frequency. Range typically [0.0, 1.0].
        c: Linear chirp rate. Range typically [0.0, 10.0].
    """
    a: float = Field(description="Cosine modulation amplitude")
    b: float = Field(description="Cosine modulation frequency")
    c: float = Field(description="Linear chirp rate")


class StepSineParams(BaseModel):
    """
    Parameters for step sine signal generation.
    
    Why: Encapsulates the frequency steps and step times needed to generate
    a step sine signal with smooth frequency transitions. Using a Pydantic
    model ensures type safety and allows validation.
    
    What: A Pydantic BaseModel containing lists of frequencies and step times
    that define a signal with piecewise constant frequencies connected by
    linear chirps for smooth transitions.
    
    Attributes:
        freq_steps: List of frequencies for each step. Typically 4 frequencies.
        step_times: List of times at which to switch frequencies. Typically 3 times.
    """
    freq_steps: List[float] = Field(description="List of frequencies for each step")
    step_times: List[float] = Field(description="List of times at which to switch frequencies")


class FreqJumpParams(BaseModel):
    """
    Parameters for frequency jump signal generation.
    
    Why: Encapsulates parameters needed to generate signals with sudden
    frequency jumps. Using a Pydantic model ensures type safety and allows
    validation of parameter ranges.
    
    What: A Pydantic BaseModel containing the number of jumps, jump times,
    and frequencies for each segment. Creates signals with sharp frequency
    transitions that appear as "dancing" in time-frequency representations.
    
    Attributes:
        n_jumps: Number of frequency jumps. Typically 3-5.
        jump_times: List of times at which frequency jumps occur.
        freqs: List of frequencies for each segment (n_jumps + 1 frequencies).
    """
    n_jumps: int = Field(description="Number of frequency jumps")
    jump_times: List[float] = Field(description="List of times at which frequency jumps occur")
    freqs: List[float] = Field(description="List of frequencies for each segment")


class SawtoothModParams(BaseModel):
    """
    Parameters for sawtooth modulation signal generation.
    
    Why: Encapsulates parameters needed to generate signals with sawtooth
    frequency modulation. Using a Pydantic model ensures type safety and
    allows validation.
    
    What: A Pydantic BaseModel containing modulation frequency, modulation
    depth, and base frequency. Creates signals with linearly varying
    frequency that creates sharp "dancing" patterns.
    
    Attributes:
        mod_freq: Frequency of the sawtooth modulation in Hz.
        mod_depth: Depth of frequency modulation (0-1 range).
        base_freq: Base frequency around which modulation occurs in Hz.
    """
    mod_freq: float = Field(description="Frequency of sawtooth modulation in Hz")
    mod_depth: float = Field(description="Depth of frequency modulation")
    base_freq: float = Field(description="Base frequency in Hz")


class SquareModParams(BaseModel):
    """
    Parameters for square wave modulation signal generation.
    
    Why: Encapsulates parameters needed to generate signals with square
    wave frequency modulation. Using a Pydantic model ensures type safety
    and allows validation.
    
    What: A Pydantic BaseModel containing modulation frequency, duty cycle,
    modulation depth, and base frequency. Creates signals with abrupt frequency
    changes that create sharp "dancing" patterns.
    
    Attributes:
        mod_freq: Frequency of the square wave modulation in Hz.
        duty_cycle: Duty cycle of the square wave (0-1 range).
        mod_depth: Depth of frequency modulation (0-1 range).
        base_freq: Base frequency around which modulation occurs in Hz.
    """
    mod_freq: float = Field(description="Frequency of square wave modulation in Hz")
    duty_cycle: float = Field(description="Duty cycle of square wave (0-1)")
    mod_depth: float = Field(description="Depth of frequency modulation")
    base_freq: float = Field(description="Base frequency in Hz")


class PhaseJumpParams(BaseModel):
    """
    Parameters for phase jump signal generation.
    
    Why: Encapsulates parameters needed to generate signals with phase
    discontinuities. Using a Pydantic model ensures type safety and allows
    validation.
    
    What: A Pydantic BaseModel containing number of jumps, jump times,
    jump sizes, and base frequency. Creates signals with sudden phase
    changes that create sharp transitions.
    
    Attributes:
        n_jumps: Number of phase jumps. Typically 2-4.
        jump_times: List of times at which phase jumps occur.
        jump_sizes: List of phase jump sizes in radians.
        base_freq: Base frequency of the signal in Hz.
    """
    n_jumps: int = Field(description="Number of phase jumps")
    jump_times: List[float] = Field(description="List of times at which phase jumps occur")
    jump_sizes: List[float] = Field(description="List of phase jump sizes in radians")
    base_freq: float = Field(description="Base frequency in Hz")


class AmplitudeModParams(BaseModel):
    """
    Parameters for amplitude modulation signal generation.
    
    Why: Encapsulates parameters needed to generate signals with amplitude
    modulation. Using a Pydantic model ensures type safety and allows
    validation.
    
    What: A Pydantic BaseModel containing modulation frequency, modulation
    depth, and base frequency. Creates signals with time-varying amplitude
    that creates dynamic "dancing" patterns.
    
    Attributes:
        mod_freq: Frequency of amplitude modulation in Hz.
        mod_depth: Depth of amplitude modulation (0-1 range).
        base_freq: Base frequency of the signal in Hz.
    """
    mod_freq: float = Field(description="Frequency of amplitude modulation in Hz")
    mod_depth: float = Field(description="Depth of amplitude modulation")
    base_freq: float = Field(description="Base frequency in Hz")


def sample_param(
    rng: np.random.Generator,
    low: float = 0.0,
    high: float = 10.0
) -> float:
    """
    Sample a single parameter from a uniform distribution.
    
    Why: Provides a reusable helper function for uniform parameter sampling,
    reducing code duplication and ensuring consistent sampling across all
    parameter generation functions.
    
    What: Samples a single float value from a uniform distribution over
    the interval [low, high) using the provided random number generator.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        low: Lower bound of the uniform distribution. Default 0.0.
        high: Upper bound of the uniform distribution. Default 10.0.
    
    Returns:
        float: A random float value in the range [low, high).
    
    Raises:
        ValueError: If low >= high.
    """
    return rng.uniform(low, high)


def gen_poly_params(
    rng: np.random.Generator,
    fmax: Optional[float] = None
) -> PolyPhaseParams:
    """
    Generate random polynomial phase parameters.
    
    Why: Encapsulates the logic for sampling valid polynomial phase parameters
    from their respective ranges. This ensures parameters are always within
    acceptable bounds for signal generation. When fmax is provided, parameters
    are constrained to ensure IFs stay within [0, fmax].
    
    What: Samples six polynomial coefficients (a, b, c, d, e, h) from uniform
    distributions over their respective ranges. If fmax is provided, scales
    the ranges to ensure the IF (kl * (b + 2ct + 3dt² + 4et³ + 5ht⁴)) stays
    within [0, fmax] for typical signal durations.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        fmax: Optional maximum frequency in Hz. If provided, constrains
            parameters to ensure IFs stay within [0, fmax]. Default None.
    
    Returns:
        PolyPhaseParams: A PolyPhaseParams object with randomly sampled
            coefficients within their valid ranges.
    """
    # Default ranges
    a_range = (-5.0, 5.0)
    b_range = (0.0, 10.0)
    c_range = (-2.0, 2.0)
    d_range = (-2.0, 2.0)
    e_range = (-1.0, 1.0)
    h_range = (-0.5, 0.5)
    
    # If fmax is provided, scale ranges to keep IF within [0, fmax]
    # Using kl=100.0 (default), IF = kl * (b + 2ct + 3dt² + 4et³ + 5ht⁴)
    # For duration=2.0s, t_max=2.0, we need to ensure IF stays in [0, fmax]
    # Conservative approach: ensure each term contributes safely
    if fmax is not None:
        kl = 100.0  # Default kl from poly_signal_and_if
        duration = 2.0  # Default duration from config
        t_max = duration
        
        # Ensure b*kl <= fmax, so b <= fmax/kl
        b_max = fmax / kl
        b_range = (0.0, min(10.0, b_max))
        
        # For higher order terms, ensure they don't push IF out of bounds
        # We need to ensure: IF = kl * (b + 2ct + 3dt² + 4et³ + 5ht⁴) stays in [0, fmax]
        # Since b >= 0, we need to ensure the sum of all terms stays in [0, fmax/kl]
        # For t in [0, t_max], we need conservative bounds on c, d, e, h
        # Strategy: allocate budget so b gets most, others get smaller shares
        total_budget = fmax / kl  # Total budget for (b + 2ct + 3dt² + 4et³ + 5ht⁴)
        
        # Reserve 60% of budget for b, 40% for other terms combined
        b_budget = total_budget * 0.6
        other_budget = total_budget * 0.4
        
        # Update b_range to use the allocated budget
        b_range = (0.0, min(10.0, b_budget))
        
        # For other terms, ensure worst-case contribution doesn't exceed budget
        # Worst case: all terms have same sign and t=t_max
        # We want: 2|c|*t_max + 3|d|*t_max² + 4|e|*t_max³ + 5|h|*t_max⁴ <= other_budget
        # Conservative: allocate equal budget to each term
        term_budget = other_budget / 4
        
        c_max = term_budget / (2 * t_max)
        c_range = (-c_max, c_max)
        
        d_max = term_budget / (3 * t_max**2)
        d_range = (-d_max, d_max)
        
        e_max = term_budget / (4 * t_max**3)
        e_range = (-e_max, e_max)
        
        h_max = term_budget / (5 * t_max**4)
        h_range = (-h_max, h_max)
    
    return PolyPhaseParams(
        a=sample_param(rng, low=a_range[0], high=a_range[1]),
        b=sample_param(rng, low=b_range[0], high=b_range[1]),
        c=sample_param(rng, low=c_range[0], high=c_range[1]),
        d=sample_param(rng, low=d_range[0], high=d_range[1]),
        e=sample_param(rng, low=e_range[0], high=e_range[1]),
        h=sample_param(rng, low=h_range[0], high=h_range[1])
    )


def gen_coschirp_params(
    rng: np.random.Generator,
    fmax: Optional[float] = None
) -> CosChirpParams:
    """
    Generate random cosine chirp parameters.
    
    Why: Encapsulates the logic for sampling valid cosine chirp parameters
    from their respective ranges. This ensures parameters are always within
    acceptable bounds for signal generation. When fmax is provided, parameters
    are constrained to ensure IFs stay within [0, fmax].
    
    What: Samples three cosine chirp coefficients (a, b, c) from uniform
    distributions over their respective ranges. If fmax is provided, scales
    the ranges to ensure the IF (Ks * (c - a*b*π² * sin(bπt + π))) stays
    within [0, fmax].
    
    Args:
        rng: NumPy random number generator for reproducibility.
        fmax: Optional maximum frequency in Hz. If provided, constrains
            parameters to ensure IFs stay within [0, fmax]. Default None.
    
    Returns:
        CosChirpParams: A CosChirpParams object with randomly sampled
            coefficients within their valid ranges.
    """
    # Default ranges
    a_range = (0.0, 2.0)
    b_range = (0.0, 2.0)
    c_range = (0.0, 20.0)
    
    # If fmax is provided, scale ranges to keep IF within [0, fmax]
    # Using Ks=5.0 (default), IF = Ks * (c - a*b*π² * sin(...))
    # Max IF is approximately Ks * (c + a*b*π²), so we need to constrain
    if fmax is not None:
        Ks = 5.0  # Default Ks from coschirp_signal_and_if
        # Scale c to ensure c*Ks <= fmax (conservative)
        c_range = (0.0, min(20.0, fmax / Ks))
        # Scale a and b to reduce modulation amplitude
        scale_factor = min(1.0, fmax / 2000.0)
        a_range = (0.0, 2.0 * scale_factor)
        b_range = (0.0, 2.0 * scale_factor)
    
    return CosChirpParams(
        a=sample_param(rng, low=a_range[0], high=a_range[1]),
        b=sample_param(rng, low=b_range[0], high=b_range[1]),
        c=sample_param(rng, low=c_range[0], high=c_range[1])
    )


def gen_step_sine_params(
    rng: np.random.Generator,
    n_steps: int = 4,
    freq_min: float = 1.0,
    freq_max: float = 1000.0,
    time_min: float = 0.25,
    time_max: float = 1.75
) -> StepSineParams:
    """
    Generate random step sine parameters.
    
    Why: Encapsulates the logic for sampling valid step sine parameters,
    including frequency steps and step times. This ensures parameters are
    always within acceptable bounds and step times are properly sorted.
    Uses uniform distribution for frequencies to ensure even coverage across
    the entire frequency range.
    
    What: Samples n_steps frequencies from [freq_min, freq_max) using uniform
    distribution for even coverage across the entire spectrum, and n_steps-1 step times
    from [time_min, time_max), then sorts the step times to ensure they are in
    ascending order. Returns a StepSineParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        n_steps: Number of frequency steps. Default 4.
        freq_min: Minimum frequency in Hz. Default 1.0.
        freq_max: Maximum frequency in Hz. Default 1000.0.
        time_min: Minimum step time in seconds. Default 0.25.
        time_max: Maximum step time in seconds. Default 1.75.
    
    Returns:
        StepSineParams: A StepSineParams object with randomly sampled
            frequencies and sorted step times.
    """
    # Use uniform distribution for even frequency coverage across entire range
    freq_steps = [
        rng.uniform(freq_min, freq_max)
        for _ in range(n_steps)
    ]
    step_times = [
        sample_param(rng, low=time_min, high=time_max)
        for _ in range(n_steps - 1)
    ]
    step_times.sort()
    return StepSineParams(freq_steps=freq_steps, step_times=step_times)


def gen_freq_jump_params(
    rng: np.random.Generator,
    n_jumps: int = None,
    freq_min: float = 1.0,
    freq_max: float = 2000.0,
    time_min: float = 0.25,
    time_max: float = 1.75
) -> FreqJumpParams:
    """
    Generate random frequency jump parameters.
    
    Why: Encapsulates the logic for sampling valid frequency jump parameters,
    including number of jumps, jump times, and frequencies. This ensures
    parameters are always within acceptable bounds and jump times are sorted.
    Uses uniform distribution for frequencies to ensure even coverage across
    the entire frequency range.
    
    What: Samples n_jumps (3-5 if not provided), jump times from [time_min, time_max),
    and n_jumps+1 frequencies from [freq_min, freq_max) using uniform distribution
    for even coverage across the entire range. Sorts jump times to ensure they are
    in ascending order. Returns a FreqJumpParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        n_jumps: Number of frequency jumps. If None, randomly samples 3-5.
        freq_min: Minimum frequency in Hz. Default 1.0.
        freq_max: Maximum frequency in Hz. Default 2000.0.
        time_min: Minimum jump time in seconds. Default 0.25.
        time_max: Maximum jump time in seconds. Default 1.75.
    
    Returns:
        FreqJumpParams: A FreqJumpParams object with randomly sampled parameters.
    """
    if n_jumps is None:
        n_jumps = rng.integers(3, 6)
    jump_times = [
        sample_param(rng, low=time_min, high=time_max)
        for _ in range(n_jumps)
    ]
    jump_times.sort()
    # Use log-uniform distribution for better frequency coverage
    log_freq_min = np.log(max(freq_min, 0.1))
    log_freq_max = np.log(freq_max)
    freqs = [
        np.exp(rng.uniform(log_freq_min, log_freq_max))
        for _ in range(n_jumps + 1)
    ]
    return FreqJumpParams(n_jumps=n_jumps, jump_times=jump_times, freqs=freqs)


def gen_sawtooth_mod_params(
    rng: np.random.Generator,
    mod_freq_range: tuple = (0.1, 10.0),
    mod_depth_range: tuple = (0.1, 0.9),
    base_freq_range: tuple = (1.0, 2000.0)
) -> SawtoothModParams:
    """
    Generate random sawtooth modulation parameters.
    
    Why: Encapsulates the logic for sampling valid sawtooth modulation
    parameters from their respective ranges. This ensures parameters are
    always within acceptable bounds for signal generation. Uses uniform
    distribution for base frequency to ensure even coverage across the entire
    frequency range.
    
    What: Samples modulation frequency, modulation depth, and base frequency
    from uniform distributions over their respective ranges. Base frequency uses
    uniform distribution for even coverage across the entire range. Returns a
    SawtoothModParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        mod_freq_range: Tuple of (min, max) for modulation frequency in Hz.
            Default (0.1, 10.0).
        mod_depth_range: Tuple of (min, max) for modulation depth. Default (0.1, 0.9).
        base_freq_range: Tuple of (min, max) for base frequency in Hz.
            Default (1.0, 2000.0).
    
    Returns:
        SawtoothModParams: A SawtoothModParams object with randomly sampled
            parameters within their valid ranges.
    """
    mod_freq = sample_param(rng, low=mod_freq_range[0], high=mod_freq_range[1])
    mod_depth = sample_param(rng, low=mod_depth_range[0], high=mod_depth_range[1])
    # Use uniform distribution for even frequency coverage across entire range
    base_freq = rng.uniform(base_freq_range[0], base_freq_range[1])
    return SawtoothModParams(
        mod_freq=mod_freq,
        mod_depth=mod_depth,
        base_freq=base_freq
    )


def gen_square_mod_params(
    rng: np.random.Generator,
    mod_freq_range: tuple = (0.1, 10.0),
    duty_cycle_range: tuple = (0.1, 0.9),
    mod_depth_range: tuple = (0.1, 0.9),
    base_freq_range: tuple = (1.0, 2000.0)
) -> SquareModParams:
    """
    Generate random square wave modulation parameters.
    
    Why: Encapsulates the logic for sampling valid square wave modulation
    parameters from their respective ranges. This ensures parameters are
    always within acceptable bounds for signal generation. Uses uniform
    distribution for base frequency to ensure even coverage across the entire
    frequency range.
    
    What: Samples modulation frequency, duty cycle, modulation depth, and
    base frequency from uniform distributions over their respective ranges.
    Base frequency uses uniform distribution for even coverage across the
    entire range. Returns a SquareModParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        mod_freq_range: Tuple of (min, max) for modulation frequency in Hz.
            Default (0.1, 10.0).
        duty_cycle_range: Tuple of (min, max) for duty cycle. Default (0.1, 0.9).
        mod_depth_range: Tuple of (min, max) for modulation depth. Default (0.1, 0.9).
        base_freq_range: Tuple of (min, max) for base frequency in Hz.
            Default (1.0, 2000.0).
    
    Returns:
        SquareModParams: A SquareModParams object with randomly sampled
            parameters within their valid ranges.
    """
    mod_freq = sample_param(rng, low=mod_freq_range[0], high=mod_freq_range[1])
    duty_cycle = sample_param(rng, low=duty_cycle_range[0], high=duty_cycle_range[1])
    mod_depth = sample_param(rng, low=mod_depth_range[0], high=mod_depth_range[1])
    # Use uniform distribution for even frequency coverage across entire range
    base_freq = rng.uniform(base_freq_range[0], base_freq_range[1])
    return SquareModParams(
        mod_freq=mod_freq,
        duty_cycle=duty_cycle,
        mod_depth=mod_depth,
        base_freq=base_freq
    )


def gen_phase_jump_params(
    rng: np.random.Generator,
    n_jumps: int = None,
    base_freq_range: tuple = (1.0, 2000.0),
    jump_size_range: tuple = (0.1, 2.0),
    time_min: float = 0.25,
    time_max: float = 1.75
) -> PhaseJumpParams:
    """
    Generate random phase jump parameters.
    
    Why: Encapsulates the logic for sampling valid phase jump parameters,
    including number of jumps, jump times, jump sizes, and base frequency.
    This ensures parameters are always within acceptable bounds and jump
    times are sorted. Uses log-uniform distribution for base frequency to
    better cover the spectrum.
    
    What: Samples n_jumps (2-4 if not provided), jump times from [time_min, time_max),
    jump sizes from [jump_size_range], and base frequency from [base_freq_range]
    using log-uniform distribution. Sorts jump times to ensure they are in
    ascending order. Returns a PhaseJumpParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        n_jumps: Number of phase jumps. If None, randomly samples 2-4.
        base_freq_range: Tuple of (min, max) for base frequency in Hz.
            Default (1.0, 2000.0).
        jump_size_range: Tuple of (min, max) for phase jump sizes in radians.
            Default (0.1, 2.0).
        time_min: Minimum jump time in seconds. Default 0.25.
        time_max: Maximum jump time in seconds. Default 1.75.
    
    Returns:
        PhaseJumpParams: A PhaseJumpParams object with randomly sampled parameters.
    """
    if n_jumps is None:
        n_jumps = rng.integers(2, 5)
    jump_times = [
        sample_param(rng, low=time_min, high=time_max)
        for _ in range(n_jumps)
    ]
    jump_times.sort()
    jump_sizes = [
        sample_param(rng, low=jump_size_range[0], high=jump_size_range[1])
        for _ in range(n_jumps)
    ]
    # Use log-uniform distribution for better frequency coverage
    log_freq_min = np.log(max(base_freq_range[0], 0.1))
    log_freq_max = np.log(base_freq_range[1])
    base_freq = np.exp(rng.uniform(log_freq_min, log_freq_max))
    return PhaseJumpParams(
        n_jumps=n_jumps,
        jump_times=jump_times,
        jump_sizes=jump_sizes,
        base_freq=base_freq
    )


def gen_amplitude_mod_params(
    rng: np.random.Generator,
    mod_freq_range: tuple = (0.1, 10.0),
    mod_depth_range: tuple = (0.1, 0.9),
    base_freq_range: tuple = (1.0, 2000.0)
) -> AmplitudeModParams:
    """
    Generate random amplitude modulation parameters.
    
    Why: Encapsulates the logic for sampling valid amplitude modulation
    parameters from their respective ranges. This ensures parameters are
    always within acceptable bounds for signal generation. Uses uniform
    distribution for base frequency to ensure even coverage across the entire
    frequency range.
    
    What: Samples modulation frequency, modulation depth, and base frequency
    from uniform distributions over their respective ranges. Base frequency uses
    uniform distribution for even coverage across the entire range. Returns an
    AmplitudeModParams object.
    
    Args:
        rng: NumPy random number generator for reproducibility.
        mod_freq_range: Tuple of (min, max) for modulation frequency in Hz.
            Default (0.1, 10.0).
        mod_depth_range: Tuple of (min, max) for modulation depth. Default (0.1, 0.9).
        base_freq_range: Tuple of (min, max) for base frequency in Hz.
            Default (1.0, 2000.0).
    
    Returns:
        AmplitudeModParams: An AmplitudeModParams object with randomly sampled
            parameters within their valid ranges.
    """
    mod_freq = sample_param(rng, low=mod_freq_range[0], high=mod_freq_range[1])
    mod_depth = sample_param(rng, low=mod_depth_range[0], high=mod_depth_range[1])
    # Use uniform distribution for even frequency coverage across entire range
    base_freq = rng.uniform(base_freq_range[0], base_freq_range[1])
    return AmplitudeModParams(
        mod_freq=mod_freq,
        mod_depth=mod_depth,
        base_freq=base_freq
    )
