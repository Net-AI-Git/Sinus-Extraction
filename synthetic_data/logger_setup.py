"""
Logging system setup for Synthetic Data Generation.

This module provides a centralized logging configuration with HTML color formatting
for Colab environments, replacing print() statements throughout the codebase.

Why: Centralized logging ensures consistent output formatting and allows easy
control over log levels. HTML color formatting in Colab provides visual
distinction between different log levels, improving readability and debugging.

What: Defines a setup_logger() function that creates and configures a logger
with HTML span-based color formatting for different log levels:
- ERROR: Red
- WARNING: Orange
- INFO: White (default)
- DEBUG: Light green
"""

import logging
from typing import Optional


def setup_logger(name: str = 'synthetic_data', level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger with HTML color formatting.
    
    Why: Provides a centralized way to configure logging throughout the
    synthetic data generation application. Ensures consistent formatting
    and prevents duplicate handlers when called multiple times. HTML color
    formatting improves readability in Colab environments.
    
    What: Creates a logger instance with HTML color formatting, removes any
    existing handlers to prevent duplicates, and configures a console handler
    with the custom formatter. The logger is ready for use throughout the
    application.
    
    Args:
        name: Logger name. Defaults to 'synthetic_data' for the main application
            logger. Use different names for different modules if needed.
        level: Logging level. Defaults to INFO. Use DEBUG for detailed output,
            WARNING for only warnings and errors, or ERROR for errors only.
    
    Returns:
        logging.Logger: Configured logger instance with HTML color formatting,
            ready for use throughout the application.
    
    Raises:
        None: This function does not raise exceptions.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    # Create simple formatter (HTML colors removed to avoid Colab JSON parsing errors)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent propagation to root logger to avoid duplicate messages
    logger.propagate = False
    
    return logger
