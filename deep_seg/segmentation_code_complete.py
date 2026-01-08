# ============================================================================
# Sinus Extraction - Image Segmentation Code
# ============================================================================

# ============================================================================
# STEP 0: Install Required Packages
# ============================================================================
!pip install segmentation-models-pytorch
!pip install -U git+https://github.com/albumentations-team/albumentations
!pip install --upgrade opencv-contrib-python
!git clone https://github.com/parth1620/Human-Segmentation-Dataset-master.git

# ============================================================================
# STEP 1: Import Libraries
# ============================================================================
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from tqdm import tqdm
import albumentations as A
from albumentations.pytorch import ToTensorV2

import segmentation_models_pytorch as smp

# ============================================================================
# STEP 2: Import Custom Modules
# ============================================================================
from config import SegmentationConfig
from logger_setup import setup_logger
from utils import load_dataframe, split_data
from dataset import SegmentationDataset
from model import create_segmentation_model
from loss_functions import CombinedLoss
from trainer import SegmentationTrainer

# ============================================================================
# STEP 3: Initialize Logger and Configuration
# ============================================================================
logger = setup_logger('segmentation', level=20)  # INFO level

# Initialize configuration
config = SegmentationConfig()

# ============================================================================
# OPTIONAL: Tune Hyperparameters for Better Performance
# ============================================================================
# Uncomment and modify the parameters below to experiment with different settings

# ===== ENCODERS (Backbone Networks) =====
# Option 1: EfficientNet - Highly efficient and often better than ResNet!
# config.encoder_name = 'efficientnet-b0'  # Smallest, fastest
# config.encoder_name = 'efficientnet-b1'  # Good balance
# config.encoder_name = 'efficientnet-b2'  # Better performance
# config.encoder_name = 'efficientnet-b3'  # Even better (slower)

# Option 2: Larger ResNet encoders (more parameters, better performance)
# config.encoder_name = 'resnet34'  # Good improvement over resnet18
# config.encoder_name = 'resnet50'  # Better but slower
# config.encoder_name = 'resnet101'  # Best but much slower

# ===== ARCHITECTURES =====
# Option 3: Try different segmentation architectures
# config.architecture = 'deeplabv3plus'  # Excellent for medical images, better boundaries
# config.architecture = 'fpn'  # Feature Pyramid Network, good for multi-scale
# config.architecture = 'linknet'  # Lightweight, fast

# ===== OPTIMIZERS =====
# Option 4: Use AdamW optimizer (often better than Adam, especially with weight decay)
# config.optimizer_name = 'adamw'

# ===== LEARNING RATE =====
# Option 5: Lower learning rate for more stable training
# config.learning_rate = 0.0005  # More stable
# config.learning_rate = 0.0001  # Very stable, slower convergence

# ===== BATCH SIZE =====
# Option 6: Adjust batch size (if you have more/less GPU memory)
# config.batch_size = 8  # smaller = more stable gradients, slower
# config.batch_size = 32  # larger = faster training, needs more memory

# ===== SCHEDULER =====
# Option 7: Adjust scheduler parameters
# config.scheduler_patience = 5  # wait longer before reducing LR
# config.scheduler_factor = 0.3  # reduce LR more aggressively

# ===== ACTIVATION =====
# Option 8: Add activation (sigmoid) - requires changing loss to BCELoss
# config.activation = 'sigmoid'  # Note: This requires modifying loss function

# ===== TRANSFER LEARNING =====
# Option 9: Control encoder freezing
# config.freeze_encoder = True   # Freeze encoder, train only decoder (default, recommended for transfer learning)
# config.freeze_encoder = False  # Train both encoder and decoder (use when you have large dataset)

# ===== RECOMMENDED COMBINATIONS =====
# Best performance (slower):
# config.encoder_name = 'efficientnet-b2'
# config.architecture = 'deeplabv3plus'
# config.optimizer_name = 'adamw'
# config.learning_rate = 0.0005

# Good balance (recommended):
# config.encoder_name = 'efficientnet-b1'
# config.architecture = 'deeplabv3plus'
# config.optimizer_name = 'adamw'
# config.learning_rate = 0.0005

# Fast and efficient:
# config.encoder_name = 'efficientnet-b0'
# config.architecture = 'unet'
# config.optimizer_name = 'adamw'

# Set random seeds for reproducibility
import random
SEED = config.seed
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

logger.info("=" * 60)
logger.info("Sinus Extraction - Image Segmentation")
logger.info("=" * 60)
logger.info(f"Random seed: {SEED} (for reproducibility)")
logger.info(f"Using device: {config.get_device()}")
logger.info(f"Model: {config.architecture} with {config.encoder_name} encoder")
logger.info(f"Pre-trained weights: {config.encoder_weights}")
logger.info(f"Freeze encoder: {config.freeze_encoder} ({'Only decoder trained' if config.freeze_encoder else 'All parameters trained'})")
logger.info(f"Batch size: {config.batch_size}, Learning rate: {config.learning_rate}")
logger.info(f"Epochs: {config.epochs}, Image size: {config.image_size}x{config.image_size}")
logger.info(f"Loss function: {config.loss_function}")
logger.info("=" * 60)

# ============================================================================
# STEP 4: Load and Split Data
# ============================================================================
import os

logger.info("Loading dataset...")

# Check if CSV file exists, if not try alternative paths
csv_path = config.csv_file_path
if not os.path.exists(csv_path):
    logger.warning(f"CSV file not found at: {csv_path}")
    # Try alternative paths
    alternative_paths = [
        '/content/Human-Segmentation-Dataset-master/train.csv',
        './Human-Segmentation-Dataset-master/train.csv',
        'Human-Segmentation-Dataset-master/train.csv',
        'train.csv'
    ]
    
    found = False
    for alt_path in alternative_paths:
        if os.path.exists(alt_path):
            csv_path = alt_path
            logger.info(f"Found CSV at alternative path: {csv_path}")
            found = True
            break
    
    if not found:
        logger.error("CSV file not found in any expected location.")
        logger.error("Please ensure the dataset is downloaded and the path is correct.")
        raise FileNotFoundError(f"CSV file not found. Tried: {csv_path} and alternatives: {alternative_paths}")

df = load_dataframe(csv_path)
logger.info(f"Loaded {len(df)} samples from CSV")

# Split data into train and validation sets
train_df, valid_df = split_data(df, test_size=0.2, random_state=SEED)
logger.info(f"Train samples: {len(train_df)}, Validation samples: {len(valid_df)}")

# ============================================================================
# STEP 5: Create Datasets and DataLoaders
# ============================================================================
# The SegmentationDataset class handles loading images and masks from paths
# It loads images as RGB and masks as grayscale, then normalizes them
logger.info("Creating datasets...")
train_dataset = SegmentationDataset(train_df, image_size=config.image_size)
valid_dataset = SegmentationDataset(valid_df, image_size=config.image_size)

# Worker init function for DataLoader reproducibility
def worker_init_fn(worker_id):
    """Initialize worker with seed for reproducibility."""
    np.random.seed(SEED + worker_id)
    random.seed(SEED + worker_id)

# Create DataLoaders for training and validation
# DataLoaders handle batching and parallel loading of images and masks
train_loader = DataLoader(
    train_dataset,
    batch_size=config.batch_size,
    shuffle=True,
    num_workers=2,
    pin_memory=True if config.device == 'cuda' else False,
    worker_init_fn=worker_init_fn
)

valid_loader = DataLoader(
    valid_dataset,
    batch_size=config.batch_size,
    shuffle=False,
    num_workers=2,
    pin_memory=True if config.device == 'cuda' else False,
    worker_init_fn=worker_init_fn
)

logger.info(f"Train batches: {len(train_loader)}, Validation batches: {len(valid_loader)}")

# ============================================================================
# STEP 6: Create Model
# ============================================================================
logger.info("Creating model...")
model = create_segmentation_model(config)
logger.info(f"Model created with {sum(p.numel() for p in model.parameters()):,} parameters")

# ============================================================================
# STEP 7: Create Trainer and Train
# ============================================================================
logger.info("Initializing trainer...")
trainer = SegmentationTrainer(model, config, logger)

logger.info("Starting training...")
history = trainer.train(
    train_loader=train_loader,
    valid_loader=valid_loader,
    checkpoint_path='best_model.pt'
)

logger.info("Training completed!")
logger.info(f"Best validation loss: {trainer.best_valid_loss:.4f}")

# ============================================================================
# STEP 8: Training Summary
# ============================================================================
logger.info("=" * 60)
logger.info("Training Summary")
logger.info("=" * 60)
logger.info(f"Total epochs trained: {len(history['train_loss'])}")
logger.info(f"Final train loss: {history['train_loss'][-1]:.4f}")
logger.info(f"Final valid loss: {history['valid_loss'][-1]:.4f}")
logger.info(f"Best valid loss: {trainer.best_valid_loss:.4f} (Model saved to 'best_model.pt')")
logger.info("=" * 60)
