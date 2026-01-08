"""
Custom exceptions for Sinus Extraction Image Segmentation.

This module defines project-specific exception classes for better error handling
and clearer error messages throughout the segmentation pipeline.

Why: Custom exceptions provide semantic meaning to errors, allowing callers to
catch and handle specific error types separately. This improves error handling
and makes debugging easier by providing clear error categories.

What: Defines a hierarchy of custom exceptions for different error types:
- ConfigError: Base exception for configuration-related errors
- DataLoadError: Errors related to loading data or datasets
- ModelError: Errors related to model creation or operations
"""


class ConfigError(Exception):
    """
    Base exception for configuration-related errors.
    
    Why: Provides a common base class for all configuration errors, allowing
    callers to catch all configuration-related issues with a single exception
    type while still maintaining specific error types for detailed handling.
    
    What: A custom exception class that inherits from Exception, providing
    a clear semantic meaning for configuration-related issues. All configuration
    errors should inherit from this class.
    """
    pass


class InvalidDeviceError(ConfigError):
    """
    Exception raised when an invalid device is specified in configuration.
    
    Why: Device validation requires checking CUDA availability, which is a
    specific error condition that should be handled explicitly. This allows
    callers to provide helpful error messages or fallback to CPU.
    
    What: Specialized exception for device-related configuration errors,
    such as requesting CUDA when it's not available or specifying an invalid
    device name.
    """
    pass


class InvalidConfigValueError(ConfigError):
    """
    Exception raised when a configuration value is invalid.
    
    Why: Configuration values must be validated to prevent runtime errors during
    training. Invalid values should be caught early with clear error messages
    that specify what went wrong and what the valid range should be.
    
    What: Specialized exception for invalid configuration parameter values,
    such as negative batch size, learning rate out of range, or invalid
    architecture name. Provides clear feedback about what went wrong.
    """
    pass


class DataLoadError(Exception):
    """
    Base exception for data loading errors.
    
    Why: Data loading can fail for various reasons (missing files, corrupted
    data, invalid format). This exception provides a common base for all
    data-related errors, allowing centralized error handling.
    
    What: A custom exception class for errors related to loading datasets,
    reading images, or processing data files. Specific data errors should
    inherit from this class.
    """
    pass


class ImageLoadError(DataLoadError):
    """
    Exception raised when an image cannot be loaded.
    
    Why: Image loading can fail due to missing files, corrupted images, or
    unsupported formats. This specific exception allows callers to handle
    image loading errors separately from other data errors.
    
    What: Specialized exception for errors that occur when attempting to
    load an image file, such as FileNotFoundError or corrupted image data.
    """
    pass


class MaskLoadError(DataLoadError):
    """
    Exception raised when a mask cannot be loaded.
    
    Why: Mask loading can fail independently of image loading, and masks
    have specific requirements (binary format, matching dimensions). This
    exception allows specific handling of mask-related errors.
    
    What: Specialized exception for errors that occur when attempting to
    load a mask file, such as missing mask files or invalid mask format.
    """
    pass


class ModelError(Exception):
    """
    Base exception for model-related errors.
    
    Why: Model creation and operations can fail for various reasons (invalid
    architecture, missing weights, device mismatch). This exception provides
    a common base for all model-related errors.
    
    What: A custom exception class for errors related to model creation,
    loading weights, or model operations. Specific model errors should
    inherit from this class.
    """
    pass


class ModelCreationError(ModelError):
    """
    Exception raised when model creation fails.
    
    Why: Model creation can fail due to invalid architecture names, incompatible
    parameters, or missing dependencies. This specific exception allows callers
    to provide helpful error messages and handle model creation failures gracefully.
    
    What: Specialized exception for errors that occur during model instantiation,
    such as invalid encoder name, incompatible input/output dimensions, or
    missing required libraries.
    """
    pass
