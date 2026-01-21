"""
Utility functions for synthetic data directory scanning and validation.

This module provides functions to scan directories, find matching sample files,
and validate array files. These utilities enable automatic dataset discovery
without requiring CSV files.

Why: Directory scanning enables automatic dataset loading without manual CSV
creation. This simplifies dataset management and allows flexible data organization
while maintaining the ability to find all samples automatically.

What: Provides functions to scan directories for samples (JPG and NPY files),
match files by UUID, validate array files, and list samples in specific scenarios.
"""

from typing import List, Tuple, Optional, Dict
import os
import re
import numpy as np
import logging

logger = logging.getLogger(__name__)


def extract_uuid_from_filename(filename: str) -> Optional[str]:
    """
    Extract UUID from filename.
    
    Why: UUIDs are used to match JPG and NPY files for the same sample.
    This function extracts the UUID from various filename formats.
    
    What: Extracts UUID pattern from filename. Supports formats:
    - {uuid}.jpg, {uuid}.npy
    - sample_{uuid}.jpg, sample_{uuid}.npy
    
    Args:
        filename: Filename (with or without path).
    
    Returns:
        Optional[str]: UUID string if found, None otherwise.
    """
    uuid_pattern = r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    match = re.search(uuid_pattern, filename, re.IGNORECASE)
    return match.group(1) if match else None


def scan_directory_for_samples(
    base_dir: str,
    freq_range: Optional[Tuple[float, float]] = None,
    scenario_name: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Scan directory structure and find all samples with matching files.
    
    Why: Enables automatic dataset discovery without CSV files. Scans the
    hierarchical directory structure to find all samples (JPG + NPY pairs).
    
    What: Scans directory structure: base_dir/freq_X_Y/scenario_name/
    and finds all samples. For each UUID, checks for existence of:
    - images/{uuid}.jpg
    - masks/{uuid}.jpg
    - arrays/stft/{uuid}.npy
    - arrays/masks/{uuid}.npy
    
    Returns list of samples with all available file paths.
    
    Args:
        base_dir: Base directory containing frequency range subdirectories.
        freq_range: Optional frequency range tuple (fmin, fmax) to filter.
            If None, scans all frequency ranges.
        scenario_name: Optional scenario name to filter. If None, scans all scenarios.
    
    Returns:
        List[Dict[str, str]]: List of sample dictionaries, each containing:
            - 'uuid': Sample UUID
            - 'image_jpg': Path to JPG image (if exists)
            - 'mask_jpg': Path to JPG mask (if exists)
            - 'stft_npy': Path to NPY STFT array (if exists)
            - 'mask_npy': Path to NPY mask array (if exists)
            - 'freq_range': Frequency range tuple
            - 'scenario': Scenario name
    
    Raises:
        OSError: If base directory cannot be accessed.
    """
    if not os.path.exists(base_dir):
        raise OSError(f"Base directory does not exist: {base_dir}")
    
    samples = []
    _scan_frequency_ranges(base_dir, freq_range, scenario_name, samples)
    return samples


def _scan_frequency_ranges(
    base_dir: str,
    freq_range: Optional[Tuple[float, float]],
    scenario_name: Optional[str],
    samples: List[Dict[str, str]]
) -> None:
    """
    Scan frequency range directories.
    
    Why: Separates frequency range scanning logic for clarity.
    
    What: Iterates over frequency range directories and calls scenario scanning.
    
    Args:
        base_dir: Base directory path.
        freq_range: Optional frequency range filter.
        scenario_name: Optional scenario name filter.
        samples: List to append found samples to.
    """
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if not os.path.isdir(item_path):
            continue
        
        if not item.startswith('freq_'):
            continue
        
        if freq_range is not None:
            parsed_range = _parse_freq_range_dir(item)
            if parsed_range != freq_range:
                continue
        
        _scan_scenarios(item_path, freq_range, scenario_name, samples)


def _parse_freq_range_dir(dir_name: str) -> Optional[Tuple[float, float]]:
    """
    Parse frequency range from directory name.
    
    Why: Extracts frequency range from directory name format: freq_X_Y.
    
    What: Parses directory name to extract (fmin, fmax) tuple.
    
    Args:
        dir_name: Directory name (e.g., 'freq_0_1000').
    
    Returns:
        Optional[Tuple[float, float]]: (fmin, fmax) if parsing succeeds, None otherwise.
    """
    pattern = r'freq_(\d+)_(\d+)'
    match = re.match(pattern, dir_name)
    if not match:
        return None
    return (float(match.group(1)), float(match.group(2)))


def _scan_scenarios(
    freq_dir: str,
    freq_range: Optional[Tuple[float, float]],
    scenario_name: Optional[str],
    samples: List[Dict[str, str]]
) -> None:
    """
    Scan scenario directories within frequency range.
    
    Why: Separates scenario scanning logic for clarity.
    
    What: Iterates over scenario directories and finds all samples.
    
    Args:
        freq_dir: Frequency range directory path.
        scenario_name: Optional scenario name filter.
        samples: List to append found samples to.
    """
    for item in os.listdir(freq_dir):
        item_path = os.path.join(freq_dir, item)
        if not os.path.isdir(item_path):
            continue
        
        if scenario_name is not None and item != scenario_name:
            continue
        
        parsed_range = _parse_freq_range_dir(os.path.basename(freq_dir))
        _find_samples_in_scenario(item_path, parsed_range, item, samples)


def _find_samples_in_scenario(
    scenario_dir: str,
    freq_range: Optional[Tuple[float, float]],
    scenario: str,
    samples: List[Dict[str, str]]
) -> None:
    """
    Find all samples in a scenario directory.
    
    Why: Separates sample finding logic for clarity.
    
    What: Scans images/ directory for JPG files, extracts UUIDs, and checks
    for corresponding files in masks/, arrays/stft/, arrays/masks/.
    
    Args:
        scenario_dir: Scenario directory path.
        freq_range: Frequency range tuple.
        scenario: Scenario name.
        samples: List to append found samples to.
    """
    images_dir = os.path.join(scenario_dir, 'images')
    if not os.path.exists(images_dir):
        return
    
    uuid_to_files = {}
    _collect_jpg_files(images_dir, uuid_to_files, 'image_jpg')
    _collect_jpg_files(os.path.join(scenario_dir, 'masks'), uuid_to_files, 'mask_jpg')
    _collect_npy_files(os.path.join(scenario_dir, 'arrays', 'stft'), uuid_to_files, 'stft_npy')
    _collect_npy_files(os.path.join(scenario_dir, 'arrays', 'masks'), uuid_to_files, 'mask_npy')
    
    for uuid_str, file_dict in uuid_to_files.items():
        sample = {
            'uuid': uuid_str,
            'freq_range': freq_range,
            'scenario': scenario,
            **file_dict
        }
        samples.append(sample)


def _collect_jpg_files(
    directory: str,
    uuid_to_files: Dict[str, Dict[str, str]],
    key: str
) -> None:
    """
    Collect JPG files and map by UUID.
    
    Why: Separates file collection logic for clarity.
    
    What: Scans directory for .jpg files, extracts UUIDs, and adds to mapping.
    
    Args:
        directory: Directory to scan.
        uuid_to_files: Dictionary mapping UUID to file paths.
        key: Key to use in file dictionary ('image_jpg' or 'mask_jpg').
    """
    if not os.path.exists(directory):
        return
    
    for filename in os.listdir(directory):
        if not filename.endswith('.jpg'):
            continue
        
        uuid_str = extract_uuid_from_filename(filename)
        if uuid_str is None:
            continue
        
        if uuid_str not in uuid_to_files:
            uuid_to_files[uuid_str] = {}
        
        uuid_to_files[uuid_str][key] = os.path.join(directory, filename)


def _collect_npy_files(
    directory: str,
    uuid_to_files: Dict[str, Dict[str, str]],
    key: str
) -> None:
    """
    Collect NPY files and map by UUID.
    
    Why: Separates file collection logic for clarity.
    
    What: Scans directory for .npy files, extracts UUIDs, and adds to mapping.
    
    Args:
        directory: Directory to scan.
        uuid_to_files: Dictionary mapping UUID to file paths.
        key: Key to use in file dictionary ('stft_npy' or 'mask_npy').
    """
    if not os.path.exists(directory):
        return
    
    for filename in os.listdir(directory):
        if not filename.endswith('.npy'):
            continue
        
        uuid_str = extract_uuid_from_filename(filename)
        if uuid_str is None:
            continue
        
        if uuid_str not in uuid_to_files:
            uuid_to_files[uuid_str] = {}
        
        uuid_to_files[uuid_str][key] = os.path.join(directory, filename)


