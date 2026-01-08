"""
Model creation for Sinus Extraction Image Segmentation.

This module provides functions for creating segmentation models using the
segmentation_models_pytorch library.

Why: Centralizing model creation ensures consistent model configuration and
makes it easy to switch between different architectures or encoders. This
module acts as a factory for model creation.

What: Provides create_segmentation_model() function that creates a UNet
model with specified encoder (ResNet18) and pre-trained ImageNet weights,
configured according to the provided configuration.
"""

import torch
import torch.nn as nn
import segmentation_models_pytorch as smp
from typing import Dict, Any
import logging

from config import SegmentationConfig
from exceptions import ModelCreationError


def create_segmentation_model(config: SegmentationConfig) -> nn.Module:
    """
    Create and return a segmentation model based on configuration.
    
    Why: Provides a centralized way to create models with consistent configuration.
    Encapsulates model creation logic and error handling, making it easy to
    switch architectures or encoders by changing the configuration.
    
    What: Creates a UNet segmentation model using segmentation_models_pytorch
    with the specified encoder (ResNet18), pre-trained ImageNet weights,
    input/output channels, and activation function from the configuration.
    The model is moved to the specified device (CPU or CUDA). If freeze_encoder
    is True in the configuration, all encoder layers are frozen to prevent
    gradient updates during training, allowing only the decoder to be trained.
    If freeze_encoder is False, all model parameters (encoder and decoder)
    will be trainable.
    
    Args:
        config: SegmentationConfig instance containing model architecture
            parameters including encoder_name, encoder_weights, architecture,
            in_channels, classes, and activation.
    
    Returns:
        nn.Module: Initialized segmentation model ready for training, moved
            to the configured device.
    
    Raises:
        ModelCreationError: If model creation fails due to invalid parameters
            or missing dependencies.
    """
    try:
        architecture_name = config.architecture.lower()
        
        if architecture_name == 'unet':
            model = smp.Unet(
                encoder_name=config.encoder_name,
                encoder_weights=config.encoder_weights,
                in_channels=config.in_channels,
                classes=config.classes,
                activation=config.activation
            )
        elif architecture_name == 'deeplabv3plus':
            model = smp.DeepLabV3Plus(
                encoder_name=config.encoder_name,
                encoder_weights=config.encoder_weights,
                in_channels=config.in_channels,
                classes=config.classes,
                activation=config.activation
            )
        elif architecture_name == 'fpn':
            model = smp.FPN(
                encoder_name=config.encoder_name,
                encoder_weights=config.encoder_weights,
                in_channels=config.in_channels,
                classes=config.classes,
                activation=config.activation
            )
        elif architecture_name == 'linknet':
            model = smp.Linknet(
                encoder_name=config.encoder_name,
                encoder_weights=config.encoder_weights,
                in_channels=config.in_channels,
                classes=config.classes,
                activation=config.activation
            )
        else:
            raise ModelCreationError(
                f"Unsupported architecture: {config.architecture}. "
                f"Supported: unet, deeplabv3plus, fpn, linknet"
            )
        
        # Move model to device
        device = config.get_device()
        model = model.to(device)
        
        # Freeze encoder layers if configured
        if config.freeze_encoder:
            _freeze_encoder_layers(model)
        
        return model
        
    except Exception as e:
        raise ModelCreationError(
            f"Failed to create segmentation model: {str(e)}"
        ) from e


def _freeze_encoder_layers(model: nn.Module) -> None:
    """
    Freeze all encoder layers to prevent gradient updates during training.
    
    Why: Freezing encoder layers is a common transfer learning practice, especially
    when using pre-trained weights. This prevents the encoder from being updated
    during training, allowing only the decoder (trained from scratch) to learn
    task-specific features. This reduces memory usage, speeds up training, and
    prevents overfitting when training data is limited.
    
    What: Iterates through all parameters in the model's encoder and sets
    requires_grad=False for each parameter, effectively freezing them. The encoder
    will remain in evaluation mode during training, using its pre-trained weights
    as fixed feature extractors.
    
    Args:
        model: Segmentation model instance with an encoder attribute. Must be
            a model from segmentation_models_pytorch (Unet, DeepLabV3Plus, FPN, Linknet).
    
    Returns:
        None: Function modifies the model in-place.
    
    Raises:
        AttributeError: If the model does not have an encoder attribute.
    """
    if not hasattr(model, 'encoder'):
        raise AttributeError(
            "Model does not have an encoder attribute. "
            "This function requires a segmentation model from segmentation_models_pytorch."
        )
    
    for param in model.encoder.parameters():
        param.requires_grad = False
    
    logger = logging.getLogger(__name__)
    logger.info("Encoder layers frozen. Only decoder will be trained.")
