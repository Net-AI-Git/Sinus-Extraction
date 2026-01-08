"""
Loss functions for Sinus Extraction Image Segmentation.

This module provides loss functions for binary segmentation, including Dice Loss,
Binary Cross Entropy, and combined losses.

Why: Segmentation tasks benefit from specialized loss functions that consider
both pixel-wise accuracy and region-based overlap. This module centralizes
loss function implementations for consistent use across training.

What: Provides DiceLoss, BCEWithLogitsLoss wrapper, and CombinedLoss classes
for binary segmentation. The combined loss (Dice + BCE) is commonly used for
segmentation tasks as it combines pixel-wise accuracy with region overlap metrics.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional


class DiceLoss(nn.Module):
    """
    Dice Loss for binary segmentation.
    
    Why: Dice Loss measures the overlap between predicted and ground truth
    regions, which is particularly important for segmentation tasks where
    we care about region accuracy, not just pixel accuracy. It helps with
    class imbalance by focusing on the overlap of positive regions.
    
    What: Implements the Dice coefficient as a loss function. The Dice
    coefficient measures the overlap between two sets, and we use 1 - Dice
    as the loss (lower is better). Includes smoothing to avoid division by zero.
    
    Attributes:
        smooth: Smoothing factor to avoid division by zero. Defaults to 1e-6.
    """
    
    def __init__(self, smooth: float = 1e-6):
        """
        Initialize DiceLoss.
        
        Why: Sets the smoothing factor which prevents division by zero when
        both prediction and target are empty (no positive pixels).
        
        What: Stores the smoothing factor for use in the forward pass.
        
        Args:
            smooth: Smoothing factor added to numerator and denominator.
                Defaults to 1e-6.
        
        Raises:
            None: This function does not raise exceptions.
        """
        super().__init__()
        self.smooth = smooth
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Compute Dice Loss.
        
        Why: Calculates the Dice coefficient between predictions and targets,
        then returns 1 - Dice as the loss. This encourages high overlap
        between predicted and ground truth regions.
        
        What: Applies sigmoid to predictions (if needed), flattens tensors,
        calculates intersection and union, and computes Dice coefficient.
        Returns 1 - Dice as the loss.
        
        Args:
            predictions: Model predictions (logits) with shape (B, C, H, W).
            targets: Ground truth masks with shape (B, C, H, W), values in [0, 1].
        
        Returns:
            torch.Tensor: Scalar Dice Loss value.
        
        Raises:
            None: This function does not raise exceptions.
        """
        # Apply sigmoid to get probabilities
        predictions = torch.sigmoid(predictions)
        
        # Flatten tensors: (B, C, H, W) -> (B*C*H*W,)
        predictions_flat = predictions.view(-1)
        targets_flat = targets.view(-1)
        
        # Calculate intersection and union
        intersection = (predictions_flat * targets_flat).sum()
        union = predictions_flat.sum() + targets_flat.sum()
        
        # Dice coefficient with smoothing
        dice = (2.0 * intersection + self.smooth) / (union + self.smooth)
        
        # Return 1 - Dice as loss
        return 1.0 - dice


class CombinedLoss(nn.Module):
    """
    Combined Dice Loss and Binary Cross Entropy Loss.
    
    Why: Combining Dice Loss (region-based) with BCE Loss (pixel-wise) provides
    better training signals. Dice Loss helps with class imbalance and region
    accuracy, while BCE Loss provides pixel-wise gradients. The combination
    often leads to better segmentation performance.
    
    What: Combines DiceLoss and BCEWithLogitsLoss with equal weighting (1:1).
    Both losses are computed and summed to create the final loss value.
    
    Attributes:
        dice_loss: DiceLoss instance for region-based loss.
        bce_loss: BCEWithLogitsLoss instance for pixel-wise loss.
    """
    
    def __init__(self, dice_smooth: float = 1e-6):
        """
        Initialize CombinedLoss.
        
        Why: Creates instances of both Dice Loss and BCE Loss to be used
        together during training.
        
        What: Initializes DiceLoss and BCEWithLogitsLoss instances with
        appropriate parameters.
        
        Args:
            dice_smooth: Smoothing factor for Dice Loss. Defaults to 1e-6.
        
        Raises:
            None: This function does not raise exceptions.
        """
        super().__init__()
        self.dice_loss = DiceLoss(smooth=dice_smooth)
        self.bce_loss = nn.BCEWithLogitsLoss()
    
    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Compute combined Dice + BCE Loss.
        
        Why: Combines both loss functions to leverage the strengths of each:
        Dice for region overlap and BCE for pixel-wise accuracy.
        
        What: Computes both Dice Loss and BCE Loss, then returns their sum.
        Both losses are weighted equally (1:1 ratio).
        
        Args:
            predictions: Model predictions (logits) with shape (B, C, H, W).
            targets: Ground truth masks with shape (B, C, H, W), values in [0, 1].
        
        Returns:
            torch.Tensor: Scalar combined loss value (Dice + BCE).
        
        Raises:
            None: This function does not raise exceptions.
        """
        dice = self.dice_loss(predictions, targets)
        bce = self.bce_loss(predictions, targets)
        return dice + bce
