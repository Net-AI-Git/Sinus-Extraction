"""
Main execution script for synthetic data generation.

This module provides the main entry point for generating synthetic data samples
and saving them to disk. It orchestrates the complete pipeline from configuration
loading to sample generation and image saving.

Why: Centralizing the main execution logic provides a clear entry point for
the application and ensures consistent execution flow. Separating batch generation
logic improves modularity and testability.

What: Provides functions to set up output directories, generate single samples,
save sample images, and execute batch generation. Includes a main() function
for command-line execution.
"""

import os
import json
from typing import Optional
import numpy as np
import logging

from .config import SyntheticDataConfig
from .logger_setup import setup_logger
from .sample_generator import generate_sample
from .visualization import save_image

logger = setup_logger('synthetic_data')
log_path = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"


def _setup_output_directories(output_dir: str) -> tuple:
    """
    Create output directories for images and masks.
    
    Why: Separates directory creation logic for clarity and testability.
    This function ensures output directories exist before saving files.
    
    What: Creates 'images' and 'masks' subdirectories within the output directory.
    Uses exist_ok=True to avoid errors if directories already exist.
    
    Args:
        output_dir: Base output directory path.
    
    Returns:
        tuple: A tuple containing (images_dir, masks_dir) paths.
    
    Raises:
        OSError: If directories cannot be created.
    """
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:52","message":"Setting up directories","data":{"output_dir":output_dir,"abs_output_dir":os.path.abspath(output_dir)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    images_dir = os.path.join(output_dir, 'images')
    masks_dir = os.path.join(output_dir, 'masks')
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:58","message":"Before makedirs","data":{"images_dir":images_dir,"masks_dir":masks_dir,"abs_images":os.path.abspath(images_dir),"abs_masks":os.path.abspath(masks_dir)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:63","message":"After makedirs","data":{"images_exists":os.path.exists(images_dir),"masks_exists":os.path.exists(masks_dir)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    return images_dir, masks_dir


def _generate_single_sample(
    rng: np.random.Generator,
    config: SyntheticDataConfig
) -> tuple:
    """
    Generate a single sample with random parameters.
    
    Why: Separates single sample generation logic for clarity and testability.
    This function handles the random parameter selection and sample generation.
    
    What: Randomly selects number of components (1-3), SNR from config.snr_list,
    and TF sigma from config.tf_sigma_range. Generates and returns the sample
    along with its parameters.
    
    Args:
        rng: NumPy random number generator.
        config: SyntheticDataConfig object.
    
    Returns:
        tuple: A tuple containing (sample, n_components, snr_db, tf_sigma).
    """
    n_components = rng.choice([1, 2, 3])
    snr_db = rng.choice(config.snr_list)
    tf_sigma = rng.uniform(
        config.tf_sigma_range[0],
        config.tf_sigma_range[1]
    )
    sample = generate_sample(
        rng, config, n_components, snr_db, tf_sigma
    )
    return sample, n_components, snr_db, tf_sigma


def _save_sample_images(
    sample: tuple,
    index: int,
    images_dir: str,
    masks_dir: str,
    config: SyntheticDataConfig
) -> None:
    """
    Save STFT and mask images for a single sample.
    
    Why: Separates image saving logic for clarity and testability.
    This function handles the file naming and image saving for both STFT
    and mask images with matching names.
    
    What: Saves the STFT spectrogram and binary mask as separate JPG files
    with matching names (sample_{index}.jpg) in their respective directories.
    
    Args:
        sample: Sample object containing STFT and binary_mask data.
        index: Sample index for filename.
        images_dir: Directory for STFT spectrogram images.
        masks_dir: Directory for binary mask images.
        config: SyntheticDataConfig object.
    
    Raises:
        IOError: If files cannot be written.
    """
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"main.py:105","message":"Saving sample","data":{"index":index,"images_dir":images_dir,"masks_dir":masks_dir},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    base_name = f'sample_{index:06d}.jpg'
    image_filename = os.path.join(images_dir, base_name)
    mask_filename = os.path.join(masks_dir, base_name)
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"main.py:112","message":"Before save_image calls","data":{"image_filename":image_filename,"mask_filename":mask_filename,"abs_image":os.path.abspath(image_filename),"abs_mask":os.path.abspath(mask_filename)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    try:
        save_image(sample.stft, image_filename, config, cmap='viridis', save_raw=True)
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:118","message":"After save_image (stft)","data":{"file_exists":os.path.exists(image_filename),"file_size":os.path.getsize(image_filename) if os.path.exists(image_filename) else 0},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
    except Exception as e:
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:123","message":"Error saving stft","data":{"error":str(e),"error_type":type(e).__name__},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
        raise
    try:
        save_image(
            sample.binary_mask,
            mask_filename,
            config,
            cmap='gray',
            title='Binary Mask',
            save_raw=True
        )
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:135","message":"After save_image (mask)","data":{"file_exists":os.path.exists(mask_filename),"file_size":os.path.getsize(mask_filename) if os.path.exists(mask_filename) else 0},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
    except Exception as e:
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"main.py:140","message":"Error saving mask","data":{"error":str(e),"error_type":type(e).__name__},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
        raise


def generate_and_save_samples(
    n_samples: int = 10000,
    config: Optional[SyntheticDataConfig] = None,
    output_dir: Optional[str] = None
) -> None:
    """
    Generate and save multiple synthetic samples.
    
    Why: Batch generation is the primary use case for synthetic data creation.
    This function orchestrates the complete pipeline from sample generation
    to image saving with progress logging.
    
    What: Sets up output directories (images/ and masks/), generates n_samples
    samples with random parameters, saves STFT and mask images with matching
    filenames (sample_{index:06d}.jpg), and logs progress every 1000 samples.
    Uses the provided config or creates a default one.
    
    Args:
        n_samples: Number of samples to generate. Default 10000.
        config: SyntheticDataConfig object. If None, creates default config.
        output_dir: Output directory path. If None, uses config.output_dir.
    
    Raises:
        OSError: If output directories cannot be created.
        SignalGenerationError: If sample generation fails.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    if output_dir is None:
        output_dir = config.output_dir
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"E","location":"main.py:160","message":"generate_and_save_samples called","data":{"n_samples":n_samples,"output_dir":output_dir,"config_output_dir":config.output_dir},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    
    images_dir, masks_dir = _setup_output_directories(output_dir)
    rng = np.random.default_rng(config.seed)
    
    logger.info(f"Starting generation of {n_samples} samples...")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Images directory: {images_dir}")
    logger.info(f"Masks directory: {masks_dir}")
    
    for i in range(n_samples):
        sample, n_comp, snr, tf_sig = _generate_single_sample(rng, config)
        _save_sample_images(sample, i, images_dir, masks_dir, config)
        
        if (i + 1) % 1000 == 0:
            logger.info(f"Generated and saved {i + 1} samples.")
    
    logger.info(f"STFT images saved to {images_dir}")
    logger.info(f"Mask images saved to {masks_dir}")
    logger.info(f"Generation complete: {n_samples} samples created.")


def main() -> None:
    """
    Main entry point for synthetic data generation.
    
    Why: Provides a standard entry point for command-line execution.
    This function loads configuration and executes batch generation.
    
    What: Creates a SyntheticDataConfig object (which can be overridden by
    environment variables), and calls generate_and_save_samples() with
    default parameters. Can be extended to accept command-line arguments.
    
    Raises:
        ConfigurationError: If configuration is invalid.
        SignalGenerationError: If sample generation fails.
    """
    config = SyntheticDataConfig()
    logger.info("Synthetic Data Generation")
    logger.info(f"Configuration: fs={config.fs}, duration={config.duration}")
    generate_and_save_samples(config=config)


if __name__ == "__main__":
    main()
