"""
Dataset class for Sinus Extraction Image Segmentation.

This module provides a PyTorch Dataset class for loading and preprocessing
segmentation images and masks from CSV file paths.

Why: PyTorch requires a Dataset class that implements __len__ and __getitem__
for DataLoader integration. This class encapsulates all image loading, preprocessing,
and format conversion logic in one place, ensuring consistent data handling.

What: Defines SegmentationDataset class that loads RGB images and binary
masks from CSV paths, and returns properly formatted tensors ready for model training.
"""

import cv2
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from typing import Optional, Tuple

from exceptions import ImageLoadError, MaskLoadError
from utils import normalize_image, normalize_mask


class SegmentationDataset(Dataset):
    """
    PyTorch Dataset for segmentation images and masks.
    
    Why: Provides a standardized way to load and preprocess segmentation data
    for training. Encapsulates all data loading logic, ensuring consistent preprocessing
    across the training pipeline.
    
    What: A Dataset class that loads RGB images and masks from CSV paths,
    normalizes both images and masks to [0, 1] range, and returns them as PyTorch
    tensors in the format expected by the model (CHW format: Channels, Height, Width).
    
    Attributes:
        df: DataFrame containing 'images' and 'masks' columns with file paths.
        image_size: Target image size for resizing. If None, uses original size.
    """
    
    def __init__(self, df: pd.DataFrame, image_size: Optional[int] = None):
        """
        Initialize SegmentationDataset.
        
        Why: Validates input dataframe and stores configuration for data loading.
        This ensures the dataset is properly configured before any data access.
        
        What: Stores the dataframe and image size configuration. Validates that
        the dataframe contains required columns.
        
        Args:
            df: DataFrame with 'images' and 'masks' columns containing file paths.
            image_size: Optional target size for resizing images. If None, uses
                original image dimensions. Defaults to None.
        
        Raises:
            ValueError: If dataframe is missing required columns.
        """
        if 'images' not in df.columns or 'masks' not in df.columns:
            raise ValueError(
                "DataFrame must contain 'images' and 'masks' columns."
            )
        
        self.df = df.reset_index(drop=True)
        self.image_size = image_size
    
    def __len__(self) -> int:
        """
        Return the number of samples in the dataset.
        
        Why: Required by PyTorch Dataset protocol. DataLoader uses this to
        determine dataset size and iteration bounds.
        
        What: Returns the number of rows in the dataframe.
        
        Returns:
            int: Number of samples in the dataset.
        
        Raises:
            None: This function does not raise exceptions.
        """
        return len(self.df)
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """
        Load and preprocess RGB image from file path.
        
        Why: Encapsulates image loading logic to avoid duplication and provide
        consistent error handling. Assumes images are RGB format from the start.
        
        What: Loads RGB image, converts from BGR (OpenCV default) to RGB format,
        optionally resizes, and normalizes to [0, 1] range.
        
        Args:
            image_path: Path to the RGB image file.
        
        Returns:
            np.ndarray: Preprocessed RGB image in (H, W, 3) format, normalized to [0, 1].
        
        Raises:
            ImageLoadError: If image cannot be loaded or is None.
        """
        # Load image as RGB (3-channel color)
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ImageLoadError(f"Could not load image: {image_path}")
        
        # Convert BGR (OpenCV default) to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize if specified
        if self.image_size is not None:
            image = cv2.resize(image, (self.image_size, self.image_size))
        
        # Normalize to [0, 1]
        image = normalize_image(image)
        
        return image
    
    def _load_mask(self, mask_path: str) -> np.ndarray:
        """
        Load and preprocess mask from file path.
        
        Why: Encapsulates mask loading logic to avoid duplication and provide
        consistent error handling. Ensures masks are properly formatted for training.
        
        What: Loads mask as grayscale, optionally resizes to match image size,
        normalizes to binary [0, 1] format, and adds channel dimension.
        
        Args:
            mask_path: Path to the mask file.
        
        Returns:
            np.ndarray: Preprocessed binary mask in (H, W, 1) format, normalized to [0, 1].
        
        Raises:
            MaskLoadError: If mask cannot be loaded or is None.
        """
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        if mask is None:
            raise MaskLoadError(f"Could not load mask: {mask_path}")
        
        # Resize if specified
        if self.image_size is not None:
            mask = cv2.resize(mask, (self.image_size, self.image_size))
        
        # Normalize to binary [0, 1]
        mask = normalize_mask(mask)
        
        # Add channel dimension: (H, W) -> (H, W, 1)
        mask = np.expand_dims(mask, axis=-1)
        
        return mask
    
    def _to_tensor(self, image: np.ndarray, mask: np.ndarray) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Convert numpy arrays to PyTorch tensors in CHW format.
        
        Why: PyTorch models expect tensors in CHW format (Channels, Height, Width),
        but images are typically loaded in HWC format. This function handles
        the conversion and ensures proper tensor types.
        
        What: Transposes arrays from HWC to CHW format and converts to PyTorch
        tensors with appropriate data types (float32 for images and masks).
        
        Args:
            image: Image array in (H, W, 3) format.
            mask: Mask array in (H, W, 1) format.
        
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: (image_tensor, mask_tensor) in
                CHW format, ready for model input.
        
        Raises:
            None: This function does not raise exceptions.
        """
        # Transpose: (H, W, C) -> (C, H, W)
        image = np.transpose(image, (2, 0, 1))
        mask = np.transpose(mask, (2, 0, 1))
        
        # Convert to tensors
        image_tensor = torch.from_numpy(image).float()
        mask_tensor = torch.from_numpy(mask).float()
        
        return image_tensor, mask_tensor
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get a single sample (image, mask) from the dataset.
        
        Why: Required by PyTorch Dataset protocol. DataLoader calls this method
        to retrieve individual samples during training. This method orchestrates
        all data loading and preprocessing steps.
        
        What: Loads RGB image and mask from paths in the dataframe, preprocesses
        them (BGR to RGB conversion, resizing if needed, normalization),
        and returns them as PyTorch tensors in CHW format.
        
        Args:
            idx: Index of the sample to retrieve.
        
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: (image, mask) tensors in CHW format,
                normalized to [0, 1] range, ready for model training.
        
        Raises:
            IndexError: If idx is out of range.
            ImageLoadError: If image cannot be loaded.
            MaskLoadError: If mask cannot be loaded.
        """
        row = self.df.iloc[idx]
        
        image_path = row['images']
        mask_path = row['masks']
        
        # Load and preprocess
        image = self._load_image(image_path)
        mask = self._load_mask(mask_path)
        
        # Convert to tensors
        image_tensor, mask_tensor = self._to_tensor(image, mask)
        
        return image_tensor, mask_tensor
