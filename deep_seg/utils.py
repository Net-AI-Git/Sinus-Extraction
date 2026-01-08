"""
Utility functions for Sinus Extraction Image Segmentation.

This module provides reusable helper functions for data processing, image conversion,
and common operations used throughout the segmentation pipeline.

Why: Centralizing utility functions prevents code duplication and ensures
consistent behavior across the codebase. These functions are designed as
independent tools that can be reused wherever needed.

What: Provides functions for:
- Converting grayscale images to RGB format for pre-trained models
- Loading and validating CSV data
- Splitting datasets into train/validation sets
- Image and mask format normalization
"""

import cv2
import numpy as np
import pandas as pd
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split

from exceptions import DataLoadError, ImageLoadError


def convert_grayscale_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convert a grayscale image to RGB format by replicating the channel.
    
    Why: Pre-trained ImageNet models expect 3-channel RGB input. Since we have
    grayscale images (1 channel) but want to use pre-trained weights, we need
    to convert single-channel images to 3-channel format by replicating the
    grayscale channel across all three RGB channels.
    
    What: Takes a grayscale image (H, W) or (H, W, 1) and converts it to
    RGB format (H, W, 3) by replicating the single channel. If the image is
    already RGB, returns it unchanged.
    
    Args:
        image: Grayscale image as numpy array. Can be 2D (H, W) or 3D (H, W, 1).
            If already 3D with 3 channels, returns unchanged.
    
    Returns:
        np.ndarray: RGB image with shape (H, W, 3). Each channel contains
            the same grayscale values.
    
    Raises:
        ValueError: If image has invalid shape (not 2D or 3D with 1 or 3 channels).
    """
    if len(image.shape) == 2:
        # 2D grayscale: (H, W) -> (H, W, 3)
        return np.stack([image] * 3, axis=-1)
    
    if len(image.shape) == 3:
        if image.shape[2] == 1:
            # 3D with 1 channel: (H, W, 1) -> (H, W, 3)
            return np.repeat(image, 3, axis=2)
        if image.shape[2] == 3:
            # Already RGB
            return image
    
    raise ValueError(
        f"Invalid image shape: {image.shape}. Expected 2D (H, W) or 3D (H, W, 1) or (H, W, 3)."
    )


def load_dataframe(csv_path: str) -> pd.DataFrame:
    """
    Load and validate CSV file containing image and mask paths.
    
    Why: CSV loading can fail for various reasons (missing file, invalid format,
    missing columns). This function provides a centralized way to load and validate
    the dataset CSV with clear error messages.
    
    What: Loads a CSV file using pandas and validates that it contains the
    required columns ('images' and 'masks'). Raises exceptions if the file
    cannot be loaded or if required columns are missing.
    
    Args:
        csv_path: Path to the CSV file containing image and mask paths.
            Expected columns: 'images' (image paths) and 'masks' (mask paths).
    
    Returns:
        pd.DataFrame: Loaded dataframe with 'images' and 'masks' columns.
    
    Raises:
        DataLoadError: If the CSV file cannot be loaded or if required columns
            are missing.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise DataLoadError(f"CSV file not found: {csv_path}")
    except pd.errors.EmptyDataError:
        raise DataLoadError(f"CSV file is empty: {csv_path}")
    except Exception as e:
        raise DataLoadError(f"Error loading CSV file {csv_path}: {str(e)}")
    
    required_columns = ['images', 'masks']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise DataLoadError(
            f"CSV file missing required columns: {missing_columns}. "
            f"Found columns: {list(df.columns)}"
        )
    
    return df


def split_data(
    dataframe: pd.DataFrame,
    test_size: float = 0.2,
    random_state: Optional[int] = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataframe into training and validation sets.
    
    Why: Dataset splitting is a common operation that should be consistent
    across the codebase. Using a fixed random_state ensures reproducibility.
    The validation set is used for hyperparameter tuning, early stopping, and
    model selection based on best validation performance.
    
    What: Uses sklearn's train_test_split to split the dataframe into training
    and validation sets. Returns two dataframes with the same structure as
    the input.
    
    Args:
        dataframe: DataFrame containing image and mask paths.
        test_size: Proportion of data to use for validation. Defaults to 0.2 (20%).
        random_state: Random seed for reproducibility. Defaults to 42.
            Set to None for non-deterministic splitting.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (train_df, valid_df) - Training
            and validation dataframes with the same structure as input.
    
    Raises:
        ValueError: If test_size is not between 0 and 1, or if dataframe is empty.
    """
    if len(dataframe) == 0:
        raise ValueError("Cannot split empty dataframe.")
    
    if not 0 < test_size < 1:
        raise ValueError(f"test_size must be between 0 and 1, got {test_size}.")
    
    train_df, valid_df = train_test_split(
        dataframe,
        test_size=test_size,
        random_state=random_state
    )
    
    return train_df, valid_df


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image to [0, 1] range and ensure float32 type.
    
    Why: Model training requires normalized images in [0, 1] range with
    consistent data type. This function ensures consistent preprocessing.
    
    What: Converts image to float32 and normalizes pixel values to [0, 1]
    range by dividing by 255.0. Handles both uint8 (0-255) and float (0-1)
    input formats.
    
    Args:
        image: Image array in uint8 (0-255) or float (0-1) format.
    
    Returns:
        np.ndarray: Normalized image in float32 format with values in [0, 1].
    
    Raises:
        None: This function does not raise exceptions.
    """
    if image.dtype == np.uint8:
        return (image.astype(np.float32) / 255.0)
    return image.astype(np.float32)


def normalize_mask(mask: np.ndarray) -> np.ndarray:
    """
    Normalize mask to binary [0, 1] range and ensure float32 type.
    
    Why: Masks need to be in binary format [0, 1] for training. This function
    ensures consistent mask preprocessing regardless of input format.
    
    What: Converts mask to float32 and normalizes to [0, 1] range. If input
    is uint8 (0-255), divides by 255.0. If already float, ensures values
    are in [0, 1] range. Binarizes by thresholding at 0.5.
    
    Args:
        mask: Mask array in uint8 (0-255) or float (0-1) format.
    
    Returns:
        np.ndarray: Binary mask in float32 format with values in [0, 1].
    
    Raises:
        None: This function does not raise exceptions.
    """
    if mask.dtype == np.uint8:
        mask = mask.astype(np.float32) / 255.0
    
    mask = mask.astype(np.float32)
    # Binarize: values > 0.5 become 1, else 0
    return (mask > 0.5).astype(np.float32)
