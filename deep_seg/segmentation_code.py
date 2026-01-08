# ============================================================================
# Sinus Extraction - Image Segmentation Code
# Ready for Google Colab - Copy all code to a single cell
# ============================================================================

# ============================================================================
# STEP 1: Install Required Packages
# ============================================================================
!pip install segmentation-models-pytorch
!pip install -U git+https://github.com/albumentations-team/albumentations
!pip install --upgrade opencv-contrib-python

# ============================================================================
# STEP 2: Clone Dataset (if needed)
# ============================================================================
!git clone https://github.com/parth1620/Human-Segmentation-Dataset-master.git

# ============================================================================
# STEP 3: Import Libraries
# ============================================================================
import sys
sys.path.append('/content/Human-Segmentation-Dataset-master')

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
# STEP 4: Import Custom Modules
# ============================================================================
# Note: In Colab, copy all module files (config.py, exceptions.py, etc.) 
# to the same directory or adjust sys.path accordingly

from config import SegmentationConfig
from logger_setup import setup_logger
from utils import load_dataframe, split_data
from dataset import SegmentationDataset
from model import create_segmentation_model
from loss_functions import CombinedLoss
from trainer import SegmentationTrainer

# ============================================================================
# STEP 5: Initialize Logger and Configuration
# ============================================================================
logger = setup_logger('segmentation', level=20)  # INFO level

# Initialize configuration
config = SegmentationConfig()

# ============================================================================
# OPTIONAL: Configure Transfer Learning
# ============================================================================
# Uncomment one of the following to control encoder freezing:
# config.freeze_encoder = True   # Freeze encoder, train only decoder (default, recommended for transfer learning)
# config.freeze_encoder = False  # Train both encoder and decoder (use when you have large dataset)

# Set random seeds for reproducibility
SEED = config.seed
import random
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
# STEP 6: Load and Split Data
# ============================================================================
logger.info("Loading dataset...")
df = load_dataframe(config.csv_file_path)
logger.info(f"Loaded {len(df)} samples from CSV")

train_df, valid_df = split_data(df, test_size=0.2, random_state=SEED)
logger.info(f"Train samples: {len(train_df)}, Validation samples: {len(valid_df)}")

# ============================================================================
# STEP 7: Create Datasets and DataLoaders
# ============================================================================
logger.info("Creating datasets...")
train_dataset = SegmentationDataset(train_df, image_size=config.image_size)
valid_dataset = SegmentationDataset(valid_df, image_size=config.image_size)

# Worker init function for DataLoader reproducibility
def worker_init_fn(worker_id):
    """Initialize worker with seed for reproducibility."""
    np.random.seed(SEED + worker_id)
    random.seed(SEED + worker_id)

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
# STEP 8: Create Model
# ============================================================================
logger.info("Creating model...")
model = create_segmentation_model(config)
logger.info(f"Model created with {sum(p.numel() for p in model.parameters()):,} parameters")

# ============================================================================
# STEP 9: Create Trainer and Train
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
# STEP 10: Training Summary
# ============================================================================
logger.info("=" * 60)
logger.info("Training Summary")
logger.info("=" * 60)
logger.info(f"Total epochs trained: {len(history['train_loss'])}")
logger.info(f"Final train loss: {history['train_loss'][-1]:.4f}")
logger.info(f"Final valid loss: {history['valid_loss'][-1]:.4f}")
logger.info(f"Best valid loss: {trainer.best_valid_loss:.4f} (Model saved to 'best_model.pt')")
logger.info("=" * 60)
