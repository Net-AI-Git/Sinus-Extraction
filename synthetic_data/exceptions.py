"""
Custom exceptions for Synthetic Data Generation.

This module defines project-specific exception classes for better error handling
and clearer error messages throughout the synthetic data generation pipeline.

Why: Custom exceptions provide semantic meaning to errors, allowing callers to
catch and handle specific error types separately. This improves error handling
and makes debugging easier by providing clear error categories.

What: Defines a hierarchy of custom exceptions for different error types:
- SyntheticDataError: Base exception for all synthetic data generation errors
- InvalidParameterError: Errors related to invalid parameter ranges
- SignalGenerationError: Errors related to signal generation failures
- ConfigurationError: Errors related to configuration validation
"""


class SyntheticDataError(Exception):
    """
    Base exception for all synthetic data generation errors.
    
    Why: Provides a common base class for all synthetic data generation errors,
    allowing callers to catch all related issues with a single exception type
    while still maintaining specific error types for detailed handling.
    
    What: A custom exception class that inherits from Exception, providing
    a clear semantic meaning for synthetic data generation-related issues.
    All synthetic data errors should inherit from this class.
    """
    pass


class InvalidParameterError(SyntheticDataError):
    """
    Exception raised when signal parameters are invalid or out of range.
    
    Why: Parameter validation requires checking IF ranges and other constraints,
    which is a specific error condition that should be handled explicitly.
    This allows callers to provide helpful error messages or retry with
    different parameters.
    
    What: Specialized exception for parameter-related errors, such as
    instantaneous frequency (IF) values outside the valid range [0, FMAX]
    or invalid parameter combinations that cannot generate valid signals.
    """
    pass


class SignalGenerationError(SyntheticDataError):
    """
    Exception raised when signal generation fails.
    
    Why: Signal generation can fail for various reasons (invalid parameters,
    numerical instability, convergence issues). This exception allows specific
    handling of signal generation failures separate from other errors.
    
    What: Specialized exception for errors that occur during signal generation,
    such as failure to find valid parameters within the maximum number of
    attempts or numerical errors during signal computation.
    """
    pass


class ConfigurationError(SyntheticDataError):
    """
    Exception raised when configuration values are invalid.
    
    Why: Configuration values must be validated to prevent runtime errors during
    data generation. Invalid values should be caught early with clear error
    messages that specify what went wrong and what the valid range should be.
    
    What: Specialized exception for invalid configuration parameter values,
    such as negative sampling rates, invalid frequency ranges, or incompatible
    parameter combinations. Provides clear feedback about what went wrong.
    """
    pass
