"""
Time-frequency representation and mask generation.

This module provides functions to convert instantaneous frequency (IF) vectors
into ideal time-frequency (TF) representations and generate binary masks
for training segmentation models.

Why: Time-frequency representations are essential for visualizing and analyzing
signals with time-varying frequency content. Binary masks derived from ideal
TF representations serve as ground truth labels for training segmentation models.

What: Provides functions to map IF vectors to ideal TF masks with Gaussian
blurring, and to generate binary masks by thresholding the ideal TF representation.
"""

from typing import List
import numpy as np
from scipy.ndimage import gaussian_filter1d


def ifs_to_ideal_tf(
    ifs_hz: List[np.ndarray],
    n_freq_bins: int = 2000,
    n_time_bins: int = 8000,
    fmax: float = 2000.0,
    sigma_bins: float = 1.0
) -> np.ndarray:
    """
    Convert instantaneous frequency vectors to ideal time-frequency mask.
    
    Why: Ideal TF representations provide ground truth labels for training
    segmentation models. Mapping IF trajectories to TF space allows visualization
    and comparison with STFT spectrograms. Gaussian blurring accounts for
    spectral spreading in real signals.
    
    What: Creates a 2D TF mask where each IF trajectory is marked as 1.0 at
    the corresponding frequency bin for each time bin. Applies Gaussian blur
    along the frequency axis to simulate spectral spreading, then normalizes
    to [0, 1] range.
    
    Args:
        ifs_hz: List of IF vectors in Hz, one per signal component. Each vector
            must have length n_time_bins.
        n_freq_bins: Number of frequency bins in output. Default 2000.
        n_time_bins: Number of time bins in output. Default 8000.
        fmax: Maximum frequency (Nyquist frequency) in Hz. Default 2000.0.
        sigma_bins: Standard deviation for Gaussian blur in frequency bins.
            Default 1.0.
    
    Returns:
        np.ndarray: Ideal TF mask, shape [n_freq_bins, n_time_bins], normalized
            to [0, 1], dtype float32.
    
    Raises:
        ValueError: If any IF vector has incorrect length or if parameters
            are invalid.
    """
    tf = np.zeros((n_freq_bins, n_time_bins), dtype=np.float32)
    for IF in ifs_hz:
        if len(IF) != n_time_bins:
            raise ValueError(
                f"IF vector length must be {n_time_bins}, got {len(IF)}."
            )
        k = np.clip(
            np.round((IF / fmax) * (n_freq_bins - 1)).astype(int),
            0,
            n_freq_bins - 1
        )
        tf[k, np.arange(n_time_bins)] = 1.0
    
    tf = gaussian_filter1d(tf, sigma=sigma_bins, axis=0, mode='nearest')
    m = tf.max() if tf.max() > 0 else 1.0
    return (tf / m).astype(np.float32)


def generate_binary_mask(
    ideal_tf: np.ndarray,
    threshold: float = 0.7
) -> np.ndarray:
    """
    Generate binary mask from ideal TF representation.
    
    Why: Binary masks are required for training segmentation models. Thresholding
    the ideal TF representation converts the continuous [0, 1] values to binary
    {0, 1} values, where 1 indicates signal presence and 0 indicates absence.
    
    What: Thresholds the ideal TF representation at the specified threshold value.
    Values above the threshold are set to 1 (white), and values below are set to 0
    (black). Returns a uint8 array for efficient storage.
    
    Args:
        ideal_tf: Ideal TF representation, shape [n_freq_bins, n_time_bins],
            values in [0, 1].
        threshold: Threshold value for binarization. Default 0.7.
            Values > threshold become 1, values <= threshold become 0.
    
    Returns:
        np.ndarray: Binary mask, shape same as ideal_tf, dtype uint8,
            values in {0, 1}.
    
    Raises:
        ValueError: If threshold is not in [0, 1] or if ideal_tf is invalid.
    """
    if not 0 <= threshold <= 1:
        raise ValueError(
            f"Threshold must be in [0, 1], got {threshold}."
        )
    return (ideal_tf > threshold).astype(np.uint8)
