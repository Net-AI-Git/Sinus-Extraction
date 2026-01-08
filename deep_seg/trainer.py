"""
Training module for Sinus Extraction Image Segmentation.

This module provides a trainer class that handles the complete training pipeline,
including training loops, validation, early stopping, and model checkpointing.

Why: Centralizing training logic ensures consistent training behavior and makes
it easy to modify training procedures. The trainer class encapsulates all training
state (optimizer, scheduler, best model) and provides a clean interface for training.

What: Defines SegmentationTrainer class that manages the complete training
process: training loop, validation loop, early stopping based on validation loss,
learning rate scheduling, and automatic model checkpointing.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Optional, Dict, Any, List
import logging
from tqdm import tqdm

from config import SegmentationConfig
from loss_functions import CombinedLoss, DiceLoss


class SegmentationTrainer:
    """
    Trainer class for segmentation model training.
    
    Why: Encapsulates all training logic in a single class, making it easy to
    manage training state, handle early stopping, and save checkpoints. Provides
    a clean interface for training while hiding implementation details.
    
    What: Manages model training with support for:
    - Training and validation loops
    - Early stopping based on validation loss
    - Learning rate scheduling
    - Automatic model checkpointing
    - Training history tracking
    
    Attributes:
        model: The segmentation model to train.
        config: Training configuration.
        loss_fn: Loss function for training.
        optimizer: Optimizer for parameter updates.
        scheduler: Learning rate scheduler (optional).
        device: Computing device (CPU or CUDA).
        best_valid_loss: Best validation loss seen so far.
        patience_counter: Counter for early stopping patience.
        train_history: Dictionary tracking training metrics.
    """
    
    def __init__(
        self,
        model: nn.Module,
        config: SegmentationConfig,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize SegmentationTrainer.
        
        Why: Sets up all training components (optimizer, loss, scheduler) based
        on configuration. This ensures consistent initialization and makes it
        easy to modify training setup.
        
        What: Creates optimizer, loss function, and scheduler based on configuration.
        Initializes training state (best loss, patience counter, history).
        
        Args:
            model: Segmentation model to train.
            config: Training configuration.
            logger: Optional logger instance. If None, creates a default logger.
        
        Raises:
            ValueError: If optimizer or loss function names are invalid.
        """
        self.model = model
        self.config = config
        self.device = config.get_device()
        self.logger = logger or logging.getLogger('trainer')
        
        # Create optimizer
        self.optimizer = self._create_optimizer()
        
        # Create loss function
        self.loss_fn = self._create_loss_function()
        
        # Create scheduler (optional)
        self.scheduler = self._create_scheduler()
        
        # Training state
        self.best_valid_loss = float('inf')
        self.patience_counter = 0
        self.train_history = {
            'train_loss': [],
            'valid_loss': []
        }
    
    def _get_decoder_parameters(self) -> List[torch.nn.Parameter]:
        """
        Extract decoder and segmentation head parameters for training.
        
        Why: When encoder is frozen, only decoder parameters should be updated
        during training. This function isolates decoder parameters so the optimizer
        can be configured to train only these layers, improving efficiency and
        preventing accidental updates to frozen encoder weights.
        
        What: Collects all parameters from the model's decoder module and
        segmentation_head module (if it exists) into a single list. These parameters
        will be used to create the optimizer, ensuring only trainable layers receive
        gradient updates.
        
        Returns:
            List[torch.nn.Parameter]: List of all decoder and segmentation head
                parameters that should be trained.
        
        Raises:
            AttributeError: If model does not have decoder attribute.
        """
        if not hasattr(self.model, 'decoder'):
            raise AttributeError(
                "Model does not have a decoder attribute. "
                "This function requires a segmentation model from segmentation_models_pytorch."
            )
        
        decoder_params = list(self.model.decoder.parameters())
        
        if hasattr(self.model, 'segmentation_head'):
            decoder_params += list(self.model.segmentation_head.parameters())
        
        return decoder_params
    
    def _create_optimizer(self) -> optim.Optimizer:
        """
        Create optimizer based on configuration.
        
        Why: Encapsulates optimizer creation logic, making it easy to switch
        optimizers or modify optimizer parameters. When encoder is frozen, only
        decoder parameters are trained, improving efficiency and preventing
        updates to frozen encoder weights. When encoder is not frozen, all
        model parameters are trained.
        
        What: Creates an optimizer (Adam, AdamW, SGD, or RMSprop) with the
        learning rate from configuration. If freeze_encoder is True, only
        decoder and segmentation head parameters are included in the optimizer.
        If freeze_encoder is False, all model parameters (encoder and decoder)
        are included in the optimizer.
        
        Returns:
            optim.Optimizer: Configured optimizer instance. If freeze_encoder
                is True, will update only decoder and segmentation head parameters.
                If False, will update all model parameters.
        
        Raises:
            ValueError: If optimizer name is invalid.
            AttributeError: If model does not have decoder attribute and
                freeze_encoder is True.
        """
        optimizer_name = self.config.optimizer_name.lower()
        lr = self.config.learning_rate
        
        # Get parameters based on freeze_encoder setting
        if self.config.freeze_encoder:
            # Only decoder parameters (encoder is frozen)
            trainable_params = self._get_decoder_parameters()
        else:
            # All model parameters (encoder and decoder)
            trainable_params = list(self.model.parameters())
        
        if optimizer_name == 'adam':
            return optim.Adam(trainable_params, lr=lr)
        elif optimizer_name == 'adamw':
            return optim.AdamW(trainable_params, lr=lr)
        elif optimizer_name == 'sgd':
            return optim.SGD(trainable_params, lr=lr, momentum=0.9)
        elif optimizer_name == 'rmsprop':
            return optim.RMSprop(trainable_params, lr=lr)
        else:
            raise ValueError(f"Invalid optimizer: {optimizer_name}")
    
    def _create_loss_function(self) -> nn.Module:
        """
        Create loss function based on configuration.
        
        Why: Encapsulates loss function creation, making it easy to switch
        between different loss functions.
        
        What: Creates loss function (CombinedLoss, DiceLoss, or BCEWithLogitsLoss)
        based on configuration.
        
        Returns:
            nn.Module: Loss function instance.
        
        Raises:
            ValueError: If loss function name is invalid.
        """
        loss_name = self.config.loss_function.lower()
        
        if loss_name == 'dice_bce':
            return CombinedLoss()
        elif loss_name == 'dice':
            return DiceLoss()
        elif loss_name == 'bce':
            return nn.BCEWithLogitsLoss()
        else:
            raise ValueError(f"Invalid loss function: {loss_name}")
    
    def _create_scheduler(self) -> Optional[optim.lr_scheduler.ReduceLROnPlateau]:
        """
        Create learning rate scheduler.
        
        Why: Learning rate scheduling helps improve convergence by reducing
        learning rate when validation loss plateaus.
        
        What: Creates a ReduceLROnPlateau scheduler that reduces learning rate
        by the configured factor when validation loss stops improving.
        
        Returns:
            Optional[optim.lr_scheduler.ReduceLROnPlateau]: Scheduler instance
                or None if scheduling is disabled.
        
        Raises:
            None: This function does not raise exceptions.
        """
        return optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=self.config.scheduler_factor,
            patience=self.config.scheduler_patience
        )
    
    def _train_epoch(self, train_loader: DataLoader, epoch: int) -> float:
        """
        Train for one epoch.
        
        Why: Encapsulates single-epoch training logic, making the training loop
        cleaner and easier to modify. Includes progress bar for visual feedback.
        
        What: Iterates through training data with progress bar, computes loss,
        performs backpropagation, and updates model parameters. Returns average
        training loss for the epoch.
        
        Args:
            train_loader: DataLoader for training data.
            epoch: Current epoch number for progress bar display.
        
        Returns:
            float: Average training loss for the epoch.
        
        Raises:
            None: This function does not raise exceptions.
        """
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        pbar = tqdm(train_loader, desc=f'Epoch {epoch} [Train]', leave=False)
        for images, masks in pbar:
            images = images.to(self.device)
            masks = masks.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            predictions = self.model(images)
            loss = self.loss_fn(predictions, masks)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
            
            # Update progress bar
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def _validate_epoch(self, valid_loader: DataLoader, epoch: int) -> float:
        """
        Validate for one epoch.
        
        Why: Encapsulates single-epoch validation logic, ensuring consistent
        validation behavior. Includes progress bar for visual feedback.
        
        What: Iterates through validation data without gradient computation,
        computes validation loss with progress bar, and returns average validation loss.
        
        Args:
            valid_loader: DataLoader for validation data.
            epoch: Current epoch number for progress bar display.
        
        Returns:
            float: Average validation loss for the epoch.
        
        Raises:
            None: This function does not raise exceptions.
        """
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        pbar = tqdm(valid_loader, desc=f'Epoch {epoch} [Valid]', leave=False)
        with torch.no_grad():
            for images, masks in pbar:
                images = images.to(self.device)
                masks = masks.to(self.device)
                
                predictions = self.model(images)
                loss = self.loss_fn(predictions, masks)
                
                total_loss += loss.item()
                num_batches += 1
                
                # Update progress bar
                pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        return total_loss / num_batches if num_batches > 0 else 0.0
    
    def _check_early_stopping(self, valid_loss: float) -> bool:
        """
        Check if early stopping condition is met.
        
        Why: Early stopping prevents overfitting by stopping training when
        validation loss stops improving. This function manages the patience
        counter and determines when to stop.
        
        What: Compares current validation loss to best validation loss.
        If improved, resets patience counter. If not improved, increments
        patience counter. Returns True if patience exceeded.
        
        Args:
            valid_loss: Current validation loss.
        
        Returns:
            bool: True if training should stop, False otherwise.
        
        Raises:
            None: This function does not raise exceptions.
        """
        if valid_loss < self.best_valid_loss:
            self.best_valid_loss = valid_loss
            self.patience_counter = 0
            return False
        else:
            self.patience_counter += 1
            return self.patience_counter >= self.config.early_stop_patience
    
    def _save_checkpoint(self, filepath: str) -> None:
        """
        Save model checkpoint.
        
        Why: Checkpointing allows resuming training or using the best model
        for inference. This function saves the complete model state.
        
        What: Saves model state dictionary to the specified filepath.
        
        Args:
            filepath: Path where to save the checkpoint.
        
        Raises:
            None: This function does not raise exceptions.
        """
        torch.save(self.model.state_dict(), filepath)
        self.logger.info(f"Model saved to {filepath}")
    
    def train(
        self,
        train_loader: DataLoader,
        valid_loader: DataLoader,
        checkpoint_path: str = 'best_model.pt'
    ) -> Dict[str, list]:
        """
        Train the model with early stopping.
        
        Why: Provides a high-level interface for training that handles all
        training logic, validation, early stopping, and checkpointing.
        
        What: Trains the model for the configured number of epochs or until
        early stopping is triggered. After each epoch, validates the model,
        updates learning rate scheduler, checks for early stopping, and saves
        checkpoints when validation loss improves.
        
        Args:
            train_loader: DataLoader for training data.
            valid_loader: DataLoader for validation data.
            checkpoint_path: Path where to save the best model checkpoint.
                Defaults to 'best_model.pt'.
        
        Returns:
            Dict[str, list]: Training history containing 'train_loss' and
                'valid_loss' lists for each epoch.
        
        Raises:
            None: This function does not raise exceptions.
        """
        self.logger.info("Starting training...")
        
        for epoch in range(1, self.config.epochs + 1):
            # Train
            train_loss = self._train_epoch(train_loader, epoch)
            
            # Validate
            valid_loss = self._validate_epoch(valid_loader, epoch)
            
            # Update scheduler
            if self.scheduler is not None:
                self.scheduler.step(valid_loss)
            
            # Log progress
            self.logger.info(
                f"Epoch {epoch}/{self.config.epochs} - "
                f"Train Loss: {train_loss:.4f}, Valid Loss: {valid_loss:.4f}"
            )
            
            # Save history
            self.train_history['train_loss'].append(train_loss)
            self.train_history['valid_loss'].append(valid_loss)
            
            # Check for improvement and save checkpoint
            if valid_loss < self.best_valid_loss:
                self._save_checkpoint(checkpoint_path)
                self.best_valid_loss = valid_loss
                self.patience_counter = 0
            else:
                self.patience_counter += 1
            
            # Check early stopping
            if self._check_early_stopping(valid_loss):
                self.logger.info(
                    f"Early stopping triggered after {epoch} epochs. "
                    f"Best validation loss: {self.best_valid_loss:.4f}"
                )
                break
        
        self.logger.info("Training completed.")
        return self.train_history
    
    def evaluate(self, test_loader: DataLoader) -> float:
        """
        Evaluate model on test set.
        
        Why: Provides a public method to evaluate the model on test data after
        training is complete. This allows final unbiased evaluation.
        
        What: Runs validation loop on test data and returns average test loss.
        
        Args:
            test_loader: DataLoader for test data.
        
        Returns:
            float: Average test loss.
        
        Raises:
            None: This function does not raise exceptions.
        """
        return self._validate_epoch(test_loader, epoch=0)
