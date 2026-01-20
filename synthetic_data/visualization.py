"""
Visualization and image saving for synthetic data.

This module provides functions to visualize and save STFT spectrograms and
binary masks as images for inspection and dataset creation.

Why: Visualization is essential for debugging and quality control of generated
samples. Image saving allows creation of datasets for training segmentation
models. Separating visualization logic improves modularity and reusability.

What: Provides functions to save individual spectrograms/masks as images and
to display multiple sample pairs side-by-side for visual inspection.
"""

from typing import List, Optional
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import logging

from .config import SyntheticDataConfig
from .sample_generator import Sample, generate_sample

logger = logging.getLogger(__name__)
log_path = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"


def save_image(
    image: np.ndarray,
    filename: str,
    config: SyntheticDataConfig,
    cmap: str = 'viridis',
    title: str = 'STFT Magnitude',
    save_raw: bool = True
) -> None:
    """
    Save a spectrogram or mask image to file.
    
    Why: Image saving is required for creating datasets for training segmentation
    models. This function provides a standardized way to save images. When
    save_raw=True, saves only the raw spectrogram without axes, labels, or
    colorbar for clean dataset images.
    
    What: Creates a matplotlib figure, displays the image with appropriate
    colormap. If save_raw=True, removes all axes, labels, and colorbar to save
    only the raw image data. Otherwise, includes axis labels and colorbar.
    Saves to the specified filename and closes the figure.
    
    Args:
        image: Image array to save, shape [n_freq_bins, n_time_bins].
        filename: Output filename (including path).
        config: SyntheticDataConfig object with duration and fmax.
        cmap: Colormap name. Default 'viridis' for spectrograms, use 'gray'
            for binary masks.
        title: Plot title. Default 'STFT Magnitude'. Only used if save_raw=False.
        save_raw: If True, saves only the raw image without axes, labels, or
            colorbar. If False, includes all formatting elements. Default True.
    
    Raises:
        IOError: If file cannot be written.
    """
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"visualization.py:60","message":"save_image called","data":{"filename":filename,"abs_filename":os.path.abspath(filename),"dir_exists":os.path.exists(os.path.dirname(filename)) if filename else False,"save_raw":save_raw},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    
    if save_raw:
        # Save raw image without any formatting
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(
            image,
            aspect='auto',
            cmap=cmap,
            origin='lower'
        )
        ax.axis('off')  # Remove all axes
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins
    else:
        # Save with full formatting
        plt.figure(figsize=(10, 8))
        plt.imshow(
            image,
            aspect='auto',
            cmap=cmap,
            origin='lower',
            extent=[0, config.duration, 0, config.fmax]
        )
        plt.colorbar(label='Magnitude')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title(title)
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"visualization.py:95","message":"Before plt.savefig","data":{"filename":filename,"abs_filename":os.path.abspath(filename),"save_raw":save_raw},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    
    if save_raw:
        plt.savefig(filename, format='jpg', bbox_inches='tight', pad_inches=0, dpi=100)
    else:
        plt.savefig(filename, format='jpg')
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"visualization.py:102","message":"After plt.savefig","data":{"file_exists":os.path.exists(filename),"abs_filename":os.path.abspath(filename),"file_size":os.path.getsize(filename) if os.path.exists(filename) else 0},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    plt.close()


def _create_subplot_figure(n_pairs: int) -> tuple:
    """
    Create matplotlib figure with subplots for sample pairs.
    
    Why: Separates figure creation logic for clarity and testability.
    This function handles the layout setup for displaying multiple sample pairs.
    
    What: Creates a figure with n_pairs rows and 2 columns (one for STFT,
    one for mask). Handles the edge case of n_pairs=1 by reshaping axes.
    
    Args:
        n_pairs: Number of sample pairs to display.
    
    Returns:
        tuple: A tuple containing (figure, axes) objects from matplotlib.
    """
    fig, axes = plt.subplots(n_pairs, 2, figsize=(16, 4 * n_pairs))
    if n_pairs == 1:
        axes = axes.reshape(1, -1)
    return fig, axes


def _plot_stft_spectrogram(
    ax: plt.Axes,
    sample: Sample,
    index: int,
    config: SyntheticDataConfig
) -> None:
    """
    Plot STFT spectrogram on a matplotlib axis.
    
    Why: Separates STFT plotting logic for clarity and reusability.
    This function handles the specific formatting for STFT spectrograms.
    
    What: Displays the STFT spectrogram with viridis colormap, adds axis
    labels, title, and colorbar. Configures the extent to match time and
    frequency ranges.
    
    Args:
        ax: Matplotlib axis to plot on.
        sample: Sample object containing STFT data.
        index: Sample index for title.
        config: SyntheticDataConfig object with duration and fmax.
    """
    im = ax.imshow(
        sample.stft,
        aspect='auto',
        cmap='viridis',
        origin='lower',
        extent=[0, config.duration, 0, config.fmax]
    )
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title(
        f'STFT Spectrogram {index + 1} '
        f'(Components: {sample.n_components})'
    )
    plt.colorbar(im, ax=ax, label='Magnitude')


def _plot_binary_mask(
    ax: plt.Axes,
    sample: Sample,
    index: int,
    config: SyntheticDataConfig
) -> None:
    """
    Plot binary mask on a matplotlib axis.
    
    Why: Separates mask plotting logic for clarity and reusability.
    This function handles the specific formatting for binary masks.
    
    What: Displays the binary mask with grayscale colormap, adds axis labels,
    title, and colorbar. Configures the extent to match time and frequency
    ranges.
    
    Args:
        ax: Matplotlib axis to plot on.
        sample: Sample object containing binary mask data.
        index: Sample index for title.
        config: SyntheticDataConfig object with duration and fmax.
    """
    im = ax.imshow(
        sample.binary_mask,
        aspect='auto',
        cmap='gray',
        origin='lower',
        extent=[0, config.duration, 0, config.fmax]
    )
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Frequency [Hz]')
    ax.set_title(f'Binary Mask {index + 1}')
    plt.colorbar(im, ax=ax, label='Mask Value')


def generate_and_display_pairs(
    samples: List[Sample],
    config: SyntheticDataConfig
) -> None:
    """
    Display multiple sample pairs side-by-side.
    
    Why: Visual inspection of generated samples is essential for quality
    control and debugging. This function provides a convenient way to
    display multiple samples for comparison.
    
    What: Creates a figure with n_pairs rows and 2 columns. For each sample,
    displays the STFT spectrogram in the left column and the binary mask
    in the right column. Applies tight layout and shows the figure.
    
    Args:
        samples: List of Sample objects to display.
        config: SyntheticDataConfig object with duration and fmax.
    
    Raises:
        ValueError: If samples list is empty.
    """
    if not samples:
        raise ValueError("Samples list cannot be empty.")
    
    n_pairs = len(samples)
    fig, axes = _create_subplot_figure(n_pairs)
    
    for i, sample in enumerate(samples):
        _plot_stft_spectrogram(axes[i, 0], sample, i, config)
        _plot_binary_mask(axes[i, 1], sample, i, config)
    
    plt.tight_layout()
    plt.show()


def generate_and_display_pairs_convenience(
    n_pairs: int = 5,
    config: Optional[SyntheticDataConfig] = None,
    seed: int = 42
) -> List[Sample]:
    """
    Generate and display sample pairs (convenience function).
    
    Why: Provides a convenient wrapper that both generates and displays samples,
    matching the original API. This simplifies usage for quick visualization
    and testing.
    
    What: Generates n_pairs samples with random parameters, then displays them
    using generate_and_display_pairs(). Returns the generated samples for
    further analysis if needed.
    
    Args:
        n_pairs: Number of sample pairs to generate and display. Default 5.
        config: SyntheticDataConfig object. If None, creates default config.
        seed: Random seed for reproducibility. Default 42.
    
    Returns:
        List[Sample]: List of generated Sample objects.
    
    Raises:
        SignalGenerationError: If sample generation fails.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    rng = np.random.default_rng(seed)
    samples = []
    
    for _ in range(n_pairs):
        n_components = rng.choice([1, 2, 3])
        snr_db = rng.choice(config.snr_list)
        tf_sigma = rng.uniform(
            config.tf_sigma_range[0],
            config.tf_sigma_range[1]
        )
        sample = generate_sample(
            rng, config, n_components, snr_db, tf_sigma
        )
        samples.append(sample)
    
    generate_and_display_pairs(samples, config)
    return samples
