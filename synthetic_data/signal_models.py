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

from typing import List
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


def gen_poly_params(rng: np.random.Generator) -> PolyPhaseParams:
    """
    Generate random polynomial phase parameters.
    
    Why: Encapsulates the logic for sampling valid polynomial phase parameters
    from their respective ranges. This ensures parameters are always within
    acceptable bounds for signal generation.
    
    What: Samples six polynomial coefficients (a, b, c, d, e, h) from uniform
    distributions over their respective ranges and returns a PolyPhaseParams
    object containing these values.
    
    Args:
        rng: NumPy random number generator for reproducibility.
    
    Returns:
        PolyPhaseParams: A PolyPhaseParams object with randomly sampled
            coefficients within their valid ranges.
    """
    return PolyPhaseParams(
        a=sample_param(rng, low=-5.0, high=5.0),
        b=sample_param(rng, low=0.0, high=10.0),
        c=sample_param(rng, low=-2.0, high=2.0),
        d=sample_param(rng, low=-1.0, high=1.0),
        e=sample_param(rng, low=-0.5, high=0.5),
        h=sample_param(rng, low=-0.2, high=0.2)
    )


def gen_coschirp_params(rng: np.random.Generator) -> CosChirpParams:
    """
    Generate random cosine chirp parameters.
    
    Why: Encapsulates the logic for sampling valid cosine chirp parameters
    from their respective ranges. This ensures parameters are always within
    acceptable bounds for signal generation.
    
    What: Samples three cosine chirp coefficients (a, b, c) from uniform
    distributions over their respective ranges and returns a CosChirpParams
    object containing these values.
    
    Args:
        rng: NumPy random number generator for reproducibility.
    
    Returns:
        CosChirpParams: A CosChirpParams object with randomly sampled
            coefficients within their valid ranges.
    """
    return CosChirpParams(
        a=sample_param(rng, low=0.0, high=1.0),
        b=sample_param(rng, low=0.0, high=1.0),
        c=sample_param(rng, low=0.0, high=10.0)
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
    
    What: Samples n_steps frequencies from [freq_min, freq_max) and n_steps-1
    step times from [time_min, time_max), then sorts the step times to ensure
    they are in ascending order. Returns a StepSineParams object.
    
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
    freq_steps = [
        sample_param(rng, low=freq_min, high=freq_max)
        for _ in range(n_steps)
    ]
    step_times = [
        sample_param(rng, low=time_min, high=time_max)
        for _ in range(n_steps - 1)
    ]
    step_times.sort()
    return StepSineParams(freq_steps=freq_steps, step_times=step_times)
