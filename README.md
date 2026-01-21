# Sinus Extraction - Image Segmentation & Synthetic Data Generation

A comprehensive project for sinus detection in images using deep learning segmentation, with a synthetic data generation pipeline for training data augmentation.

## Project Overview

This project consists of two main components:

1. **Deep Segmentation Module** (`deep_seg/`): UNet-based segmentation model with ResNet18 encoder for detecting sinuses in grayscale images
2. **Synthetic Data Generation Module** (`synthetic_data/`): Pipeline for generating synthetic sine wave signals with various modulation types, noise levels, and time-frequency representations (STFT)

## Features

### Deep Segmentation
- UNet architecture with ResNet18 backbone
- Pre-trained ImageNet weights support
- Optimized for grayscale image segmentation
- Comprehensive logging system with HTML color formatting
- Type-safe configuration using dataclasses
- Custom exception handling
- Data augmentation pipeline
- Ready for Google Colab with GPU support

### Synthetic Data Generation
- Multiple signal scenarios (pure sine, amplitude modulation, frequency modulation, etc.)
- Configurable SNR levels for noise addition
- STFT (Short-Time Fourier Transform) representation
- Hierarchical output directory structure
- Parallel processing with ProcessPoolExecutor
- Balanced dataset generation
- Type-safe configuration using pydantic-settings
- Environment variable support for configuration

## Installation

### Requirements

```bash
pip install -r requirements.txt
```

### Dependencies

- `numpy>=1.21.0`
- `matplotlib>=3.5.0`
- `scipy>=1.7.0`
- `pydantic>=2.0.0`
- `pydantic-settings>=2.0.0`
- `torch` (for deep segmentation - install separately)
- `segmentation-models-pytorch` (for deep segmentation - install separately)

## Project Structure

```
Sinus-Extraction/
├── deep_seg/                    # Deep segmentation module
│   ├── config.py               # Segmentation configuration
│   ├── dataset.py              # Dataset classes
│   ├── model.py                # UNet model definition
│   ├── trainer.py              # Training pipeline
│   ├── loss_functions.py       # Custom loss functions
│   ├── utils.py                # Utility functions
│   ├── logger_setup.py         # Logging configuration
│   ├── exceptions.py           # Custom exceptions
│   └── run_in_colab.ipynb      # Colab notebook
│
├── synthetic_data/              # Synthetic data generation module
│   ├── config.py               # Configuration (pydantic-settings)
│   ├── main.py                 # Main execution script
│   ├── sample_generator.py     # Sample generation logic
│   ├── signal_generators.py    # Signal generation functions
│   ├── signal_models.py        # Signal model definitions
│   ├── signal_processing.py    # Signal processing utilities
│   ├── tf_representation.py   # Time-frequency representations
│   ├── visualization.py        # Visualization functions
│   ├── utils.py                # Utility functions
│   ├── logger_setup.py         # Logging configuration
│   └── exceptions.py           # Custom exceptions
│
├── Segmentation_code_templates/ # Jupyter notebook templates
│   ├── ImageSegmentation_template.ipynb
│   └── Deep_Learning_with_PyTorch_ImageSegmentation.ipynb
│
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Usage

### Synthetic Data Generation

Generate synthetic data samples for training:

```bash
# Basic usage (default: 5 samples per directory)
python -m synthetic_data.main

# Custom number of samples per directory
python -m synthetic_data.main --samples_per_directory 100

# Custom output directory
python -m synthetic_data.main --output_dir /path/to/output --samples_per_directory 50

# Custom number of parallel workers
python -m synthetic_data.main --samples_per_directory 100 --max_workers 8
```

#### Configuration

The synthetic data generation uses `pydantic-settings` for configuration. You can override settings via environment variables or a `.env` file:

```bash
# Example environment variables
export SYNTHETIC_DATA_FS=4000
export SYNTHETIC_DATA_DURATION=2.0
export SYNTHETIC_DATA_OUTPUT_DIR=/path/to/output
```

#### Output Structure

The generated data follows a hierarchical structure:

```
output_dir/
└── freq_X_Y/                    # Frequency range (e.g., freq_100_500)
    └── scenario_name/           # Signal scenario (e.g., pure_sine)
        ├── images/              # STFT images (JPG)
        ├── masks/               # Mask images (JPG)
        └── arrays/
            ├── stft/            # STFT arrays (NPY)
            └── masks/           # Mask arrays (NPY)
```

### Deep Segmentation (Google Colab)

#### Load the notebook directly from GitHub:

1. Open [Google Colab](https://colab.research.google.com/)
2. Click **File** → **Open notebook**
3. Select the **GitHub** tab
4. Paste the repository URL:
   ```
   https://github.com/Net-AI-Git/Sinus-Extraction
   ```
5. Select the notebook: `Segmentation_code_templates/ImageSegmentation_template.ipynb`
6. Click **Open**

#### Direct link to Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Net-AI-Git/Sinus-Extraction/blob/main/Segmentation_code_templates/ImageSegmentation_template.ipynb)

Or copy this link:
```
https://colab.research.google.com/github/Net-AI-Git/Sinus-Extraction/blob/main/Segmentation_code_templates/ImageSegmentation_template.ipynb
```

#### Updating the Notebook

When you make changes to the notebook and push them to GitHub:

1. In Colab, click **File** → **Revert to last saved version** (if you have unsaved changes)
2. Or refresh the page (F5) to load the new version from GitHub

### Deep Segmentation (Local)

You can also run the segmentation code locally:

```python
from deep_seg.config import SegmentationConfig
from deep_seg.trainer import SegmentationTrainer
from deep_seg.dataset import SegmentationDataset

# Create configuration
config = SegmentationConfig(
    encoder_name="resnet18",
    encoder_weights="imagenet",
    # ... other parameters
)

# Initialize trainer
trainer = SegmentationTrainer(config)

# Train the model
trainer.train()
```

## Configuration

### Synthetic Data Configuration

The `SyntheticDataConfig` class (in `synthetic_data/config.py`) supports:
- Signal parameters (sampling rate, duration, frequency ranges)
- SNR levels for noise addition
- STFT parameters (window size, overlap, FFT size)
- Output directory paths
- Signal scenarios (pure sine, AM, FM, etc.)

### Segmentation Configuration

The `SegmentationConfig` class (in `deep_seg/config.py`) supports:
- Model architecture (encoder, decoder)
- Training hyperparameters (learning rate, batch size, epochs)
- Data paths (train, validation, test)
- Augmentation settings
- Loss function selection

## Development Standards

This project follows strict coding standards:

- **Function Length**: All functions must be under 20 lines
- **Type Hints**: Full type hinting for all functions and variables
- **Async I/O**: Uses `asyncio` for I/O-bound operations
- **Parallel Processing**: Uses `ProcessPoolExecutor` for CPU-bound operations
- **Logging**: Structured logging with no `print()` statements
- **Error Handling**: Comprehensive error classification and retry logic
- **Documentation**: Comprehensive docstrings for all public functions

## Notes

- The segmentation model is optimized for grayscale image segmentation
- Training from scratch (no pre-trained weights) for grayscale images
- Includes data augmentation, custom dataset, and training pipeline
- Synthetic data generation supports parallel processing for faster generation
- All configuration is type-safe and validated

## License

[Add your license information here]

## Contributing

[Add contributing guidelines here]
