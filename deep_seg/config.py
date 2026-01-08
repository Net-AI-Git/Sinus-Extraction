"""
Configuration module for Sinus Extraction Image Segmentation.

This module provides a type-safe configuration dataclass for the segmentation
training pipeline, including model architecture, training hyperparameters, and
data paths.

Why: Centralized configuration management ensures consistency across the codebase,
enables easy experimentation with different hyperparameters, and provides type
safety and validation to catch configuration errors early.

What: Defines a SegmentationConfig dataclass that encapsulates all configuration
parameters for the segmentation model, including encoder selection (ResNet18),
architecture (UNet), training settings (Adam optimizer, learning rate, batch size),
and data paths. Includes validation logic to ensure all values are within acceptable
ranges.
"""

from dataclasses import dataclass
from typing import Optional
import torch

from exceptions import InvalidDeviceError, InvalidConfigValueError


@dataclass
class SegmentationConfig:
    """
    Type-safe configuration container for segmentation model training.
    
    Why: Using a dataclass provides type safety, validation, and clear documentation
    of all configuration parameters. This prevents runtime errors from typos or
    invalid values and makes the configuration self-documenting. The configuration
    is optimized for grayscale image segmentation with pre-trained ImageNet weights
    by converting single-channel images to 3-channel format.
    
    What: A dataclass that encapsulates all hyperparameters and model settings
    for the segmentation training pipeline. Configured for binary segmentation
    of sinuses in grayscale images using UNet architecture with ResNet18 encoder
    and ImageNet pre-trained weights. The configuration includes validation logic
    in __post_init__ to ensure all values are within acceptable ranges.
    
    Attributes:
        encoder_name: Name of the encoder backbone. ResNet18 is chosen as a
            lightweight, efficient backbone that works well with pre-trained
            ImageNet weights. It provides good feature extraction while being
            fast to train and requiring less memory than larger models.
        encoder_weights: Pre-trained weights to use. 'imagenet' enables transfer
            learning from ImageNet, which significantly improves performance
            especially when training data is limited. Since we convert grayscale
            to 3-channel RGB, we can leverage these pre-trained weights.
        architecture: Segmentation architecture name. 'unet' is chosen for its
            excellent performance on medical image segmentation tasks, with
            skip connections that preserve fine details and spatial information.
        in_channels: Number of input image channels. Set to 3 to match pre-trained
            ImageNet weights. Grayscale images will be converted to 3-channel
            format by replicating the single channel.
        classes: Number of output classes. Set to 1 for binary segmentation
            (sinus vs. background).
        activation: Activation function for model output. None means no activation
            is applied in the model, allowing the loss function (BCEWithLogitsLoss)
            to handle the sigmoid activation internally for numerical stability.
        device: Computing device ('cuda' or 'cpu'). CUDA is preferred for GPU
            acceleration, which significantly speeds up training.
        batch_size: Number of samples per training batch. 16 is chosen as a balance
            between training stability, memory usage, and gradient estimation quality
            for Colab GPU environments.
        learning_rate: Initial learning rate for optimizer. 0.001 is a standard
            starting point for Adam optimizer, providing good convergence speed
            while remaining stable.
        epochs: Maximum number of training epochs. 40 provides sufficient training
            time while allowing early stopping to prevent overfitting.
        early_stop_patience: Number of epochs without improvement before stopping
            training. 7 epochs provides a good balance between allowing the model
            to recover from temporary plateaus and preventing unnecessary training
            when the model has converged.
        image_size: Target image size for training. 256x256 is chosen as a standard
            size that balances detail preservation with computational efficiency
            and memory constraints.
        csv_file_path: Path to the CSV file containing image and mask paths.
            Configured for Colab environment at '/content/Human-Segmentation-Dataset-master/train.csv'.
        data_dir: Root directory for data storage. Configured for Colab at '/content/'.
        optimizer_name: Name of the optimizer. 'adam' is chosen for its adaptive
            learning rate and good performance across various tasks without
            extensive hyperparameter tuning.
        loss_function: Loss function configuration. 'dice_bce' indicates using
            a combination of Dice Loss and Binary Cross Entropy, which provides
            good performance for segmentation tasks by combining pixel-wise
            accuracy (BCE) with region-based overlap (Dice).
        use_augmentations: Whether to apply data augmentations. Set to False as
            per requirements, though augmentations are typically beneficial for
            small datasets.
        scheduler_factor: Factor by which learning rate is reduced when using
        a learning rate scheduler. 0.5 means halving the learning rate.
        scheduler_patience: Number of epochs to wait before reducing learning rate
        when using a scheduler. 3 epochs provides a reasonable wait time
        before adjusting the learning rate.
        freeze_encoder: Whether to freeze encoder layers during training. If True,
            encoder parameters are frozen and only decoder is trained. If False,
            all model parameters (encoder and decoder) are trainable. Default is
            True to enable transfer learning with pre-trained encoder weights.
    """
    
    # Model Architecture Configuration
    encoder_name: str = 'resnet18'
    encoder_weights: str = 'imagenet'
    architecture: str = 'unet'
    in_channels: int = 3
    classes: int = 1
    activation: Optional[str] = None
    
    # Training Configuration
    device: str = 'cuda'
    batch_size: int = 16
    learning_rate: float = 0.001
    epochs: int = 40
    early_stop_patience: int = 7
    
    # Data Configuration
    image_size: int = 256
    csv_file_path: str = '/content/Human-Segmentation-Dataset-master/train.csv'
    data_dir: str = '/content/'
    
    # Optimizer and Loss Configuration
    optimizer_name: str = 'adam'
    loss_function: str = 'dice_bce'
    
    # Augmentation Configuration
    use_augmentations: bool = False
    
    # Learning Rate Scheduler Configuration
    scheduler_factor: float = 0.5
    scheduler_patience: int = 3
    
    # Transfer Learning Configuration
    freeze_encoder: bool = True  # If True, encoder layers are frozen and only decoder is trained
    
    # Random Seed Configuration
    seed: int = 42
    
    def __post_init__(self) -> None:
        """
        Validate configuration values after initialization.
        
        Why: Ensures all configuration values are valid before they are used,
        catching errors early and providing clear feedback. This prevents
        runtime errors during training that could waste computational resources.
        
        What: Performs validation checks on all configuration parameters:
        - Validates device availability (CUDA if requested)
        - Ensures positive values for batch size, learning rate, epochs, etc.
        - Validates that early stop patience is positive
        - Checks that image size is reasonable
        - Validates encoder and architecture names are supported
        - Ensures loss function and optimizer names are valid
        
        Raises:
            InvalidDeviceError: If CUDA is requested but not available.
            InvalidConfigValueError: If any configuration value is invalid or out of range.
        """
        # Validate device
        if self.device == 'cuda' and not torch.cuda.is_available():
            raise InvalidDeviceError(
                "CUDA device requested but not available. "
                "Set device='cpu' or ensure CUDA is properly configured."
            )
        
        if self.device not in ['cuda', 'cpu']:
            raise InvalidConfigValueError(
                f"Invalid device: {self.device}. Must be 'cuda' or 'cpu'."
            )
        
        # Validate positive numeric values
        if self.batch_size <= 0:
            raise InvalidConfigValueError(
                f"Batch size must be positive, got {self.batch_size}."
            )
        
        if self.learning_rate <= 0:
            raise InvalidConfigValueError(
                f"Learning rate must be positive, got {self.learning_rate}."
            )
        
        if self.epochs <= 0:
            raise InvalidConfigValueError(
                f"Epochs must be positive, got {self.epochs}."
            )
        
        if self.early_stop_patience <= 0:
            raise InvalidConfigValueError(
                f"Early stop patience must be positive, got {self.early_stop_patience}."
            )
        
        if self.image_size <= 0:
            raise InvalidConfigValueError(
                f"Image size must be positive, got {self.image_size}."
            )
        
        # Validate image size is reasonable (power of 2 is common)
        if self.image_size < 64 or self.image_size > 1024:
            raise InvalidConfigValueError(
                f"Image size {self.image_size} is outside recommended range [64, 1024]. "
                "Consider using a size between 64 and 1024 pixels."
            )
        
        # Validate in_channels
        if self.in_channels not in [1, 3]:
            raise InvalidConfigValueError(
                f"in_channels must be 1 or 3, got {self.in_channels}. "
                "For grayscale with pre-trained weights, use 3 (grayscale will be converted)."
            )
        
        # Validate classes
        if self.classes <= 0:
            raise InvalidConfigValueError(
                f"Number of classes must be positive, got {self.classes}."
            )
        
        # Validate optimizer name
        valid_optimizers = ['adam', 'adamw', 'sgd', 'rmsprop']
        if self.optimizer_name.lower() not in valid_optimizers:
            raise InvalidConfigValueError(
                f"Invalid optimizer: {self.optimizer_name}. "
                f"Must be one of {valid_optimizers}."
            )
        
        # Validate loss function
        valid_losses = ['dice_bce', 'bce', 'dice', 'focal']
        if self.loss_function.lower() not in valid_losses:
            raise InvalidConfigValueError(
                f"Invalid loss function: {self.loss_function}. "
                f"Must be one of {valid_losses}."
            )
        
        # Validate architecture
        valid_architectures = ['unet', 'deeplabv3plus', 'fpn', 'linknet']
        if self.architecture.lower() not in valid_architectures:
            raise InvalidConfigValueError(
                f"Invalid architecture: {self.architecture}. "
                f"Must be one of {valid_architectures}."
            )
        
        # Validate scheduler parameters
        if not 0 < self.scheduler_factor < 1:
            raise InvalidConfigValueError(
                f"Scheduler factor must be between 0 and 1, got {self.scheduler_factor}."
            )
        
        if self.scheduler_patience <= 0:
            raise InvalidConfigValueError(
                f"Scheduler patience must be positive, got {self.scheduler_patience}."
            )
        
        # Validate seed
        if self.seed < 0:
            raise InvalidConfigValueError(
                f"Seed must be non-negative, got {self.seed}."
            )
    
    def get_device(self) -> torch.device:
        """
        Get PyTorch device object from configuration.
        
        Why: Provides a convenient method to convert the string device name
        to a PyTorch device object, which is required for model and tensor
        operations.
        
        What: Converts the device string ('cuda' or 'cpu') to a torch.device
        object that can be used directly in PyTorch operations.
        
        Returns:
            torch.device: PyTorch device object corresponding to the configured device.
        
        Raises:
            RuntimeError: If CUDA is requested but not available (should be
                caught in __post_init__, but included here for safety).
        """
        return torch.device(self.device)
