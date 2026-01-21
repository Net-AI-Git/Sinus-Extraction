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
import sys
import json
import uuid
import warnings
from typing import Optional, Tuple, List, Dict, Any
import numpy as np
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

# Suppress RuntimeWarning about module import in multiprocessing
# This warning occurs when ProcessPoolExecutor imports modules in worker processes
# It's harmless but noisy, so we suppress it globally
warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')

# Handle both direct execution and package import
if __name__ == "__main__":
    # When running directly, add parent directory to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from synthetic_data.config import SyntheticDataConfig
    from synthetic_data.logger_setup import setup_logger
    from synthetic_data.sample_generator import generate_sample
    from synthetic_data.visualization import save_image
else:
    # When imported as module, use relative imports
    from .config import SyntheticDataConfig
    from .logger_setup import setup_logger
    from .sample_generator import generate_sample
    from .visualization import save_image

logger = setup_logger('synthetic_data')
log_path = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"

def _debug_log(location: str, message: str, data: Dict[str, Any], hypothesis_id: str = "A") -> None:
    """Helper function to write debug logs in NDJSON format."""
    try:
        import time
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Silently fail if logging doesn't work


def _setup_hierarchical_directories(
    base_output_dir: str,
    freq_range: Tuple[float, float],
    scenario_name: str
) -> Tuple[str, str, str, str]:
    """
    Create hierarchical output directories for frequency range and scenario.
    
    Why: Organizes output data hierarchically by frequency range and signal
    scenario, enabling organized dataset structure and easy filtering. Creates
    directories for both image (JPG) and array (NPY) formats.
    
    What: Creates directory structure: base_output_dir/freq_X_Y/scenario_name/
    with subdirectories: images/, masks/, arrays/stft/, arrays/masks/.
    Uses exist_ok=True to avoid errors if directories already exist.
    
    Args:
        base_output_dir: Base output directory path.
        freq_range: Frequency range tuple (fmin, fmax).
        scenario_name: Signal scenario name.
    
    Returns:
        Tuple[str, str, str, str]: A tuple containing (images_dir, masks_dir,
            stft_arrays_dir, mask_arrays_dir) paths.
    
    Raises:
        OSError: If directories cannot be created.
    """
    config = SyntheticDataConfig()
    freq_dir_name = config.get_freq_range_dir_name(freq_range[0], freq_range[1])
    scenario_dir = os.path.join(base_output_dir, freq_dir_name, scenario_name)
    images_dir = os.path.join(scenario_dir, 'images')
    masks_dir = os.path.join(scenario_dir, 'masks')
    arrays_dir = os.path.join(scenario_dir, 'arrays')
    stft_arrays_dir = os.path.join(arrays_dir, 'stft')
    mask_arrays_dir = os.path.join(arrays_dir, 'masks')
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    os.makedirs(stft_arrays_dir, exist_ok=True)
    os.makedirs(mask_arrays_dir, exist_ok=True)
    
    return images_dir, masks_dir, stft_arrays_dir, mask_arrays_dir


def _save_sample_dual_format(
    sample: 'Sample',
    unique_id: str,
    images_dir: str,
    masks_dir: str,
    stft_arrays_dir: str,
    mask_arrays_dir: str,
    config: SyntheticDataConfig
) -> None:
    """
    Save sample in both JPG (images) and NPY (arrays) formats.
    
    Why: Enables dual format storage for backward compatibility (JPG) and
    precise training (NPY). This function encapsulates the saving logic
    to avoid duplication across multiple generation functions.
    
    What: Saves STFT and binary mask as both JPG images and NPY arrays
    using the same UUID for matching. JPG files use {uuid}.jpg naming,
    NPY files use {uuid}.npy naming.
    
    Args:
        sample: Sample object containing STFT and binary_mask data.
        unique_id: UUID string for file naming.
        images_dir: Directory for STFT JPG images.
        masks_dir: Directory for mask JPG images.
        stft_arrays_dir: Directory for STFT NPY arrays.
        mask_arrays_dir: Directory for mask NPY arrays.
        config: SyntheticDataConfig object.
    
    Raises:
        IOError: If files cannot be written.
    """
    image_jpg_path = os.path.join(images_dir, f'{unique_id}.jpg')
    mask_jpg_path = os.path.join(masks_dir, f'{unique_id}.jpg')
    stft_npy_path = os.path.join(stft_arrays_dir, f'{unique_id}.npy')
    mask_npy_path = os.path.join(mask_arrays_dir, f'{unique_id}.npy')
    
    save_image(sample.stft, image_jpg_path, config, cmap='viridis', save_raw=True)
    save_image(
        sample.binary_mask,
        mask_jpg_path,
        config,
        cmap='gray',
        title='Binary Mask',
        save_raw=True
    )
    
    from .visualization import save_array
    save_array(sample.stft, stft_npy_path)
    save_array(sample.binary_mask.astype(np.float32), mask_npy_path)


def generate_samples_by_scenario(
    scenario_name: str,
    freq_range: Tuple[float, float],
    n_samples: int,
    config: Optional[SyntheticDataConfig] = None,
    base_output_dir: Optional[str] = None,
    n_components: int = 1
) -> None:
    """
    Generate samples for a specific scenario and frequency range.
    
    Why: Enables targeted generation of specific signal types within specific
    frequency ranges. This supports organized dataset creation with consistent
    image dimensions per frequency range.
    
    What: Generates n_samples of the specified scenario in the specified
    freq_range. Uses freq_range-specific n_freq_bins, nfft, and fmax for
    consistent image dimensions. Creates hierarchical directory structure
    and saves all samples to the appropriate location.
    
    Args:
        scenario_name: Signal scenario name (e.g., 'poly_phase', 'freq_jump').
        freq_range: Frequency range tuple (fmin, fmax).
        n_samples: Number of samples to generate.
        config: SyntheticDataConfig object. If None, creates default config.
        base_output_dir: Base output directory. If None, uses config.output_dir.
        n_components: Number of signal components. Default 1.
    
    Raises:
        OSError: If directories cannot be created.
        SignalGenerationError: If sample generation fails.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    if base_output_dir is None:
        base_output_dir = config.output_dir
    
    images_dir, masks_dir, stft_arrays_dir, mask_arrays_dir = _setup_hierarchical_directories(
        base_output_dir, freq_range, scenario_name
    )
    rng = np.random.default_rng(config.seed)
    
    n_freq_bins = config.get_n_freq_bins_for_range(freq_range[1])
    nfft = config.get_nfft_for_range(freq_range[1])
    fmax = freq_range[1]
    
    logger.info(
        f"Generating {n_samples} samples: scenario={scenario_name}, "
        f"freq_range={freq_range}, n_freq_bins={n_freq_bins}, nfft={nfft}"
    )
    
    for i in range(n_samples):
        snr_db = rng.choice(config.snr_list)
        tf_sigma = rng.uniform(
            config.tf_sigma_range[0],
            config.tf_sigma_range[1]
        )
        sample = generate_sample(
            rng,
            config,
            n_components,
            snr_db,
            tf_sigma,
            signal_scenario=scenario_name,
            freq_range=freq_range
        )
        unique_id = str(uuid.uuid4())
        _save_sample_dual_format(
            sample,
            unique_id,
            images_dir,
            masks_dir,
            stft_arrays_dir,
            mask_arrays_dir,
            config
        )
        
        if (i + 1) % 1000 == 0:
            logger.info(f"Generated and saved {i + 1} samples.")
    
    logger.info(f"Generation complete: {n_samples} samples saved to {scenario_name}")


def generate_all_scenarios(
    n_samples_per_scenario: int = 1000,
    config: Optional[SyntheticDataConfig] = None,
    base_output_dir: Optional[str] = None
) -> None:
    """
    Generate samples for all scenarios and frequency ranges.
    
    Why: Provides a convenient way to generate a complete dataset covering
    all signal types and frequency ranges. This ensures comprehensive coverage
    for training segmentation models.
    
    What: Iterates over all freq_ranges and signal_scenarios in the config,
    calling generate_samples_by_scenario() for each combination. Generates
    n_samples_per_scenario samples for each scenario-range combination.
    
    Args:
        n_samples_per_scenario: Number of samples to generate per scenario-range
            combination. Default 1000.
        config: SyntheticDataConfig object. If None, creates default config.
        base_output_dir: Base output directory. If None, uses config.output_dir.
    
    Raises:
        OSError: If directories cannot be created.
        SignalGenerationError: If sample generation fails.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    if base_output_dir is None:
        base_output_dir = config.output_dir
    
    total_combinations = len(config.freq_ranges) * len(config.signal_scenarios)
    logger.info(
        f"Generating complete dataset: {total_combinations} combinations, "
        f"{n_samples_per_scenario} samples each"
    )
    
    combination_count = 0
    for freq_range in config.freq_ranges:
        for scenario in config.signal_scenarios:
            combination_count += 1
            logger.info(
                f"Combination {combination_count}/{total_combinations}: "
                f"{scenario} in {freq_range}"
            )
            generate_samples_by_scenario(
                scenario,
                freq_range,
                n_samples_per_scenario,
                config,
                base_output_dir,
                n_components=1
            )
    
    logger.info(f"Complete dataset generation finished: {total_combinations} combinations")


def _generate_and_save_single_sample(
    task_params: Dict[str, Any]
) -> Tuple[str, str, int, str]:
    """
    Generate and save a single sample (for parallel processing).
    
    Why: This function is designed to be picklable for ProcessPoolExecutor.
    It receives all necessary parameters as a dictionary and creates a new
    RNG instance to avoid pickling issues. Enhanced error handling provides
    detailed error information for debugging.
    
    What: Creates a new RNG from the provided seed, generates a sample with
    the specified parameters, saves both STFT and mask images, and returns
    status information with error type for better error tracking.
    
    Args:
        task_params: Dictionary containing all parameters needed for sample
            generation: seed, config_dict, n_components, snr_db, tf_sigma,
            signal_scenario, freq_range, images_dir, masks_dir, sample_index,
            total_samples, combination_info.
    
    Returns:
        Tuple[str, str, int, str]: (status, message, sample_index, error_type)
            where error_type is empty string if success, or exception type name if error.
    """
    # Import here to avoid pickling issues
    import os
    import uuid
    import numpy as np
    from synthetic_data.config import SyntheticDataConfig
    from synthetic_data.sample_generator import generate_sample
    from synthetic_data.visualization import save_image, save_array
    
    try:
        # Reconstruct config from dict
        config = SyntheticDataConfig(**task_params['config_dict'])
        
        # Create new RNG with task-specific seed
        rng = np.random.default_rng(task_params['seed'])
        
        # Generate sample
        sample = generate_sample(
            rng,
            config,
            task_params['n_components'],
            task_params['snr_db'],
            task_params['tf_sigma'],
            signal_scenario=task_params['signal_scenario'],
            freq_range=task_params['freq_range']
        )
        
        # Generate unique ID and save
        unique_id = str(uuid.uuid4())
        image_jpg_path = os.path.join(task_params['images_dir'], f'{unique_id}.jpg')
        mask_jpg_path = os.path.join(task_params['masks_dir'], f'{unique_id}.jpg')
        stft_npy_path = os.path.join(task_params['stft_arrays_dir'], f'{unique_id}.npy')
        mask_npy_path = os.path.join(task_params['mask_arrays_dir'], f'{unique_id}.npy')
        
        save_image(
            sample.stft,
            image_jpg_path,
            config,
            cmap='viridis',
            save_raw=True
        )
        save_image(
            sample.binary_mask,
            mask_jpg_path,
            config,
            cmap='gray',
            title='Binary Mask',
            save_raw=True
        )
        save_array(sample.stft, stft_npy_path)
        save_array(sample.binary_mask.astype(np.float32), mask_npy_path)
        
        return (
            'success',
            f"Sample {task_params['sample_index']}/{task_params['total_samples']}: "
            f"{task_params['combination_info']} - {unique_id}",
            task_params['sample_index'],
            ''
        )
    except Exception as e:
        error_type = type(e).__name__
        return (
            'error',
            f"Error generating sample {task_params['sample_index']}: {str(e)}",
            task_params['sample_index'],
            error_type
        )


def generate_diverse_samples(
    n_samples: int = 3,
    config: Optional[SyntheticDataConfig] = None,
    base_output_dir: Optional[str] = None,
    max_workers: Optional[int] = None
) -> None:
    """
    Generate diverse samples systematically across all frequency ranges and scenarios.
    
    Why: Provides a convenient way to generate a diverse dataset with systematic
    coverage of all frequency ranges and signal scenarios. This ensures
    comprehensive coverage while maintaining the hierarchical directory structure.
    The order is fixed (deterministic), but signal parameters are randomized.
    Uses parallel processing to speed up generation.
    
    What: Iterates over all freq_ranges and signal_scenarios in fixed order.
    For each combination, generates n_samples with random signal parameters
    (frequencies, amplitudes, modulation depths, etc.) using parallel processing.
    Each sample is saved to the appropriate hierarchical directory structure
    (freq_X_Y/scenario/images|masks). Logs progress for each generated sample.
    
    Args:
        n_samples: Number of samples to generate per (freq_range, scenario)
            combination. Default 3.
        config: SyntheticDataConfig object. If None, creates default config.
        base_output_dir: Base output directory. If None, uses config.output_dir.
        max_workers: Maximum number of parallel workers. If None, uses
            os.cpu_count(). Default None.
    
    Raises:
        OSError: If directories cannot be created.
        SignalGenerationError: If sample generation fails.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    if base_output_dir is None:
        base_output_dir = config.output_dir
    
    if max_workers is None:
        max_workers = os.cpu_count() or 4
    
    # Exclude 'mixed' scenario for systematic generation
    scenarios = [s for s in config.signal_scenarios if s != 'mixed']
    
    total_combinations = len(config.freq_ranges) * len(scenarios)
    total_samples = total_combinations * n_samples
    
    logger.info(
        f"Generating {total_samples} samples ({n_samples} per combination) "
        f"across {total_combinations} (freq_range, scenario) combinations..."
    )
    logger.info(f"Output directory: {base_output_dir}")
    logger.info(f"Using {max_workers} parallel workers")
    
    # Prepare all tasks
    tasks = []
    rng = np.random.default_rng(config.seed)
    sample_index = 0
    
    # Convert config to dict for pickling
    # Support both Pydantic v1 (dict()) and v2 (model_dump())
    if hasattr(config, 'model_dump'):
        config_dict = config.model_dump()
    else:
        config_dict = config.dict()
    
    # Iterate over all frequency ranges in fixed order
    for freq_range in config.freq_ranges:
        fmin, fmax = freq_range
        
        # Iterate over all scenarios in fixed order
        for scenario in scenarios:
            # Setup hierarchical directories for this combination
            images_dir, masks_dir, stft_arrays_dir, mask_arrays_dir = _setup_hierarchical_directories(
                base_output_dir,
                freq_range,
                scenario
            )
            
            combination_info = f"{scenario} in {freq_range}"
            
            # Generate n_samples for this combination with random parameters
            for i in range(n_samples):
                sample_index += 1
                
                # Random parameters for this sample (generate seed for this task)
                task_seed = rng.integers(0, 2**31)
                task_rng = np.random.default_rng(task_seed)
                
                n_components = task_rng.choice([1, 2, 3])
                snr_db = task_rng.choice(config.snr_list)
                tf_sigma = task_rng.uniform(
                    config.tf_sigma_range[0],
                    config.tf_sigma_range[1]
                )
                
                # Create task parameters
                task_params = {
                    'seed': task_seed,
                    'config_dict': config_dict,
                    'n_components': int(n_components),
                    'snr_db': float(snr_db),
                    'tf_sigma': float(tf_sigma),
                    'signal_scenario': scenario,
                    'freq_range': freq_range,
                    'images_dir': images_dir,
                    'masks_dir': masks_dir,
                    'stft_arrays_dir': stft_arrays_dir,
                    'mask_arrays_dir': mask_arrays_dir,
                    'sample_index': sample_index,
                    'total_samples': total_samples,
                    'combination_info': combination_info
                }
                
                tasks.append(task_params)
    
    # Execute tasks in parallel
    completed_count = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(_generate_and_save_single_sample, task): task
            for task in tasks
        }
        
        # Process completed tasks as they finish
        for future in as_completed(futures):
            status, message, sample_idx, error_type = future.result()
            completed_count += 1
            
            if status == 'success':
                logger.info(message)
            else:
                logger.error(message)
            
            # Progress update every 100 samples
            if completed_count % 100 == 0 or completed_count == total_samples:
                logger.info(
                    f"Progress: {completed_count}/{total_samples} samples completed "
                    f"({100.0 * completed_count / total_samples:.1f}%)"
                )
    
    logger.info(f"Generation complete: {total_samples} samples created.")
    logger.info(
        f"Coverage: {len(config.freq_ranges)} frequency ranges × "
        f"{len(scenarios)} scenarios × {n_samples} samples each"
    )


def _generate_multiple_samples_for_directory(
    task_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate multiple samples for a single directory (for parallel processing).
    
    Why: This function is designed to be picklable for ProcessPoolExecutor.
    It generates a fixed number of samples for a single (freq_range, scenario)
    combination, ensuring balanced dataset generation. Each directory gets
    exactly the same number of samples.
    
    What: Creates a new RNG from base seed, generates exactly samples_count
    samples with deterministic seeds (base_seed + i), saves all samples to
    the appropriate directory, and returns statistics about success/errors.
    
    Args:
        task_params: Dictionary containing: freq_range, scenario, samples_count,
            config_dict, base_seed, images_dir, masks_dir, stft_arrays_dir,
            mask_arrays_dir, combination_info.
    
    Returns:
        Dict[str, Any]: Statistics dictionary with keys: success_count, error_count,
            errors (list of error messages), combination_info, directory_path.
    """
    # Import here to avoid pickling issues and RuntimeWarning
    import os
    import uuid
    import numpy as np
    import json
    import time
    import warnings
    # Suppress RuntimeWarning about module import in multiprocessing
    warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')
    from synthetic_data.config import SyntheticDataConfig
    from synthetic_data.sample_generator import generate_sample
    from synthetic_data.visualization import save_image, save_array
    
    # #region agent log
    try:
        log_path_local = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "A",
            "location": "main.py:_generate_multiple_samples_for_directory:ENTRY",
            "message": "Function entry",
            "data": {
                "scenario": task_params.get('scenario', 'unknown'),
                "samples_count": task_params.get('samples_count', 0),
                "base_seed": task_params.get('base_seed', 0),
                "images_dir": task_params.get('images_dir', 'unknown')
            },
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path_local, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    freq_range = task_params['freq_range']
    scenario = task_params['scenario']
    samples_count = task_params['samples_count']
    config_dict = task_params['config_dict']
    base_seed = task_params['base_seed']
    images_dir = task_params['images_dir']
    masks_dir = task_params['masks_dir']
    stft_arrays_dir = task_params['stft_arrays_dir']
    mask_arrays_dir = task_params['mask_arrays_dir']
    combination_info = task_params['combination_info']
    
    # Reconstruct config from dict
    config = SyntheticDataConfig(**config_dict)
    
    success_count = 0
    error_count = 0
    errors = []
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "B",
            "location": "main.py:_generate_multiple_samples_for_directory:BEFORE_LOOP",
            "message": "Before sample generation loop",
            "data": {
                "samples_count": samples_count,
                "config_loaded": True
            },
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path_local, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    # Generate exactly samples_count samples
    for i in range(samples_count):
        # Create deterministic seed for this sample
        sample_seed = base_seed + i
        rng = np.random.default_rng(sample_seed)
        
        # Random parameters for this sample
        n_components = rng.choice([1, 2, 3])
        snr_db = rng.choice(config.snr_list)
        tf_sigma = rng.uniform(
            config.tf_sigma_range[0],
            config.tf_sigma_range[1]
        )
        
        # #region agent log
        try:
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "N",
                "location": "main.py:_generate_multiple_samples_for_directory:BEFORE_GENERATE",
                "message": "Before generate_sample call",
                "data": {
                    "sample_index": i + 1,
                    "total_samples": samples_count,
                    "sample_seed": sample_seed,
                    "n_components": int(n_components),
                    "snr_db": float(snr_db),
                    "tf_sigma": float(tf_sigma),
                    "scenario": scenario,
                    "freq_range": freq_range,
                    "fmax": freq_range[1] if freq_range else None
                },
                "timestamp": int(time.time() * 1000)
            }
            with open(log_path_local, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass
        # #endregion
        
        try:
            # Generate sample
            sample = generate_sample(
                rng,
                config,
                int(n_components),
                float(snr_db),
                float(tf_sigma),
                signal_scenario=scenario,
                freq_range=freq_range
            )
            
            # Generate unique ID and save
            unique_id = str(uuid.uuid4())
            image_jpg_path = os.path.join(images_dir, f'{unique_id}.jpg')
            mask_jpg_path = os.path.join(masks_dir, f'{unique_id}.jpg')
            stft_npy_path = os.path.join(stft_arrays_dir, f'{unique_id}.npy')
            mask_npy_path = os.path.join(mask_arrays_dir, f'{unique_id}.npy')
            
            save_image(
                sample.stft,
                image_jpg_path,
                config,
                cmap='viridis',
                save_raw=True
            )
            save_image(
                sample.binary_mask,
                mask_jpg_path,
                config,
                cmap='gray',
                title='Binary Mask',
                save_raw=True
            )
            save_array(sample.stft, stft_npy_path)
            save_array(sample.binary_mask.astype(np.float32), mask_npy_path)
            
            success_count += 1
            
            # #region agent log
            try:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "C",
                    "location": "main.py:_generate_multiple_samples_for_directory:SAMPLE_SUCCESS",
                    "message": "Sample generated successfully",
                    "data": {
                        "sample_index": i + 1,
                        "total_samples": samples_count,
                        "success_count": success_count,
                        "unique_id": unique_id
                    },
                    "timestamp": int(time.time() * 1000)
                }
                with open(log_path_local, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception:
                pass
            # #endregion
        except Exception as e:
            error_type = type(e).__name__
            error_count += 1
            error_msg = f"Sample {i+1}/{samples_count} failed: {str(e)} ({error_type})"
            errors.append(error_msg)
            
            # #region agent log
            try:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": "D",
                    "location": "main.py:_generate_multiple_samples_for_directory:SAMPLE_ERROR",
                    "message": "Sample generation failed",
                    "data": {
                        "sample_index": i + 1,
                        "total_samples": samples_count,
                        "error_type": error_type,
                        "error_message": str(e),
                        "error_count": error_count,
                        "sample_seed": sample_seed,
                        "n_components": int(n_components),
                        "snr_db": float(snr_db),
                        "scenario": scenario,
                        "freq_range": freq_range
                    },
                    "timestamp": int(time.time() * 1000)
                }
                with open(log_path_local, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception:
                pass
            # #endregion
    
    result = {
        'success_count': success_count,
        'error_count': error_count,
        'errors': errors,
        'combination_info': combination_info,
        'directory_path': images_dir
    }
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "E",
            "location": "main.py:_generate_multiple_samples_for_directory:EXIT",
            "message": "Function exit",
            "data": {
                "success_count": success_count,
                "error_count": error_count,
                "total_samples": samples_count,
                "combination_info": combination_info
            },
            "timestamp": int(time.time() * 1000)
        }
        with open(log_path_local, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    return result


def generate_balanced_dataset(
    samples_per_directory: int = 5,
    config: Optional[SyntheticDataConfig] = None,
    base_output_dir: Optional[str] = None,
    max_workers: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate balanced dataset with equal number of samples per directory.
    
    Why: Ensures every (freq_range, scenario) combination has exactly the same
    number of samples, creating a balanced dataset for training. Uses parallel
    processing to speed up generation significantly.
    
    What: Creates tasks for each (freq_range, scenario) combination, where each
    task generates exactly samples_per_directory samples. Executes all tasks
    in parallel using ProcessPoolExecutor. Skips errors and continues. Reports
    progress every 100 completed samples. Returns statistics at the end.
    
    Args:
        samples_per_directory: Number of samples to generate per directory.
            Default 5. Easy to change for different dataset sizes.
        config: SyntheticDataConfig object. If None, creates default config.
        base_output_dir: Base output directory. If None, uses config.output_dir.
        max_workers: Maximum number of parallel workers. If None, uses
            os.cpu_count(). Default None.
    
    Returns:
        Dict[str, Any]: Statistics dictionary with keys: total_directories,
            total_samples_expected, total_samples_success, total_samples_errors,
            directories_completed, directories_with_errors, errors_summary.
    
    Raises:
        OSError: If output directories cannot be created.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    if base_output_dir is None:
        base_output_dir = config.output_dir
    
    if max_workers is None:
        max_workers = os.cpu_count() or 4
    
    # Exclude 'mixed' scenario
    scenarios = [s for s in config.signal_scenarios if s != 'mixed']
    
    total_combinations = len(config.freq_ranges) * len(scenarios)
    total_samples_expected = total_combinations * samples_per_directory
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "G",
            "location": "main.py:generate_balanced_dataset:CONFIG_CALC",
            "message": "Configuration calculated",
            "data": {
                "total_combinations": total_combinations,
                "total_samples_expected": total_samples_expected,
                "num_freq_ranges": len(config.freq_ranges),
                "num_scenarios": len(scenarios),
                "max_workers": max_workers
            },
            "timestamp": int(__import__('time').time() * 1000)
        }
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    logger.info(
        f"Generating balanced dataset: {samples_per_directory} samples per directory"
    )
    logger.info(
        f"Total: {total_combinations} directories × {samples_per_directory} samples = "
        f"{total_samples_expected} samples"
    )
    logger.info(f"Output directory: {base_output_dir}")
    logger.info(f"Using {max_workers} parallel workers")
    
    # Prepare all tasks
    tasks = []
    rng = np.random.default_rng(config.seed)
    task_index = 0
    
    # Convert config to dict for pickling
    if hasattr(config, 'model_dump'):
        config_dict = config.model_dump()
    else:
        config_dict = config.dict()
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "H",
            "location": "main.py:generate_balanced_dataset:BEFORE_TASK_CREATION",
            "message": "Before task creation loop",
            "data": {
                "config_dict_keys": list(config_dict.keys())[:5] if config_dict else []
            },
            "timestamp": int(__import__('time').time() * 1000)
        }
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    # Create task for each (freq_range, scenario) combination
    for freq_range in config.freq_ranges:
        for scenario in scenarios:
            # Setup hierarchical directories
            images_dir, masks_dir, stft_arrays_dir, mask_arrays_dir = _setup_hierarchical_directories(
                base_output_dir,
                freq_range,
                scenario
            )
            
            combination_info = f"{scenario} in {freq_range}"
            
            # Generate base seed for this task (deterministic)
            task_seed = rng.integers(0, 2**31)
            
            task_params = {
                'freq_range': freq_range,
                'scenario': scenario,
                'samples_count': samples_per_directory,
                'config_dict': config_dict,
                'base_seed': task_seed,
                'images_dir': images_dir,
                'masks_dir': masks_dir,
                'stft_arrays_dir': stft_arrays_dir,
                'mask_arrays_dir': mask_arrays_dir,
                'combination_info': combination_info
            }
            
            tasks.append(task_params)
            task_index += 1
    
    # Execute tasks in parallel
    completed_count = 0
    total_success = 0
    total_errors = 0
    directories_completed = 0
    directories_with_errors = 0
    all_errors = []
    last_reported_samples = 0
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(_generate_multiple_samples_for_directory, task): task
            for task in tasks
        }
        
        # Process completed tasks as they finish
        for future in as_completed(futures):
            try:
                result = future.result()
                completed_count += 1
                directories_completed += 1
                
                # #region agent log
                try:
                    log_entry = {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "K",
                        "location": "main.py:generate_balanced_dataset:TASK_COMPLETED",
                        "message": "Task completed",
                        "data": {
                            "completed_count": completed_count,
                            "total_combinations": total_combinations,
                            "success_count": result['success_count'],
                            "error_count": result['error_count'],
                            "combination_info": result['combination_info']
                        },
                        "timestamp": int(__import__('time').time() * 1000)
                    }
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(log_entry) + "\n")
                except Exception:
                    pass
                # #endregion
                
                total_success += result['success_count']
                total_errors += result['error_count']
                
                if result['error_count'] > 0:
                    directories_with_errors += 1
                    all_errors.extend(result['errors'])
                    logger.warning(
                        f"Directory {result['combination_info']}: "
                        f"{result['success_count']} success, {result['error_count']} errors"
                    )
                else:
                    logger.info(
                        f"Directory {result['combination_info']}: "
                        f"{result['success_count']} samples generated successfully"
                    )
                
                # Progress update every 100 samples
                if (total_success - last_reported_samples >= 100 or 
                    completed_count == total_combinations):
                    progress_pct = 100.0 * completed_count / total_combinations
                    samples_pct = 100.0 * total_success / total_samples_expected
                    logger.info(
                        f"Progress: {completed_count}/{total_combinations} directories "
                        f"({progress_pct:.1f}%), {total_success}/{total_samples_expected} samples "
                        f"({samples_pct:.1f}%), {total_errors} errors"
                    )
                    last_reported_samples = total_success
            except Exception as e:
                completed_count += 1
                directories_with_errors += 1
                error_type = type(e).__name__
                error_msg = f"Task execution failed: {str(e)} ({error_type})"
                all_errors.append(error_msg)
                logger.error(error_msg)
                # #region agent log
                try:
                    log_entry = {
                        "sessionId": "debug-session",
                        "runId": "run1",
                        "hypothesisId": "L",
                        "location": "main.py:generate_balanced_dataset:TASK_ERROR",
                        "message": "Task execution error",
                        "data": {
                            "error_type": error_type,
                            "error_message": str(e),
                            "completed_count": completed_count
                        },
                        "timestamp": int(__import__('time').time() * 1000)
                    }
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(log_entry) + "\n")
                except Exception:
                    pass
                # #endregion
    
    # Final statistics
    stats = {
        'total_directories': total_combinations,
        'total_samples_expected': total_samples_expected,
        'total_samples_success': total_success,
        'total_samples_errors': total_errors,
        'directories_completed': directories_completed,
        'directories_with_errors': directories_with_errors,
        'errors_summary': all_errors[:10] if len(all_errors) > 10 else all_errors
    }
    
    # #region agent log
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "M",
            "location": "main.py:generate_balanced_dataset:EXIT",
            "message": "Function exit with statistics",
            "data": stats,
            "timestamp": int(__import__('time').time() * 1000)
        }
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass
    # #endregion
    
    logger.info(f"Generation complete!")
    logger.info(f"Directories: {directories_completed}/{total_combinations} completed")
    logger.info(f"Samples: {total_success}/{total_samples_expected} generated successfully")
    if total_errors > 0:
        logger.warning(f"Errors: {total_errors} samples failed")
    
    return stats


def verify_dataset_balance(
    base_output_dir: str,
    expected_samples_per_dir: int,
    config: Optional[SyntheticDataConfig] = None
) -> Dict[str, Any]:
    """
    Verify dataset balance by counting images in each directory.
    
    Why: Ensures the dataset is balanced by checking that every directory
    contains exactly the expected number of samples. This validation step
    catches any generation issues or missing files.
    
    What: Scans all directories in the hierarchical structure (freq_X_Y/scenario/images),
    counts images in each directory, identifies directories with incorrect counts,
    and returns a detailed report with statistics.
    
    Args:
        base_output_dir: Base output directory to scan.
        expected_samples_per_dir: Expected number of images per directory.
        config: SyntheticDataConfig object. If None, creates default config.
    
    Returns:
        Dict[str, Any]: Verification report with keys: total_directories,
            balanced_directories, unbalanced_directories, missing_directories,
            directory_counts (dict mapping dir_path to count), summary.
    """
    if config is None:
        config = SyntheticDataConfig()
    
    # Exclude 'mixed' scenario
    scenarios = [s for s in config.signal_scenarios if s != 'mixed']
    
    directory_counts = {}
    balanced_directories = []
    unbalanced_directories = []
    missing_directories = []
    
    # Scan all directories
    for freq_range in config.freq_ranges:
        freq_dir_name = config.get_freq_range_dir_name(freq_range[0], freq_range[1])
        
        for scenario in scenarios:
            images_dir = os.path.join(
                base_output_dir,
                freq_dir_name,
                scenario,
                'images'
            )
            
            if not os.path.exists(images_dir):
                missing_directories.append(images_dir)
                continue
            
            # Count image files
            image_files = [
                f for f in os.listdir(images_dir)
                if f.endswith('.jpg') or f.endswith('.png')
            ]
            count = len(image_files)
            directory_counts[images_dir] = count
            
            if count == expected_samples_per_dir:
                balanced_directories.append(images_dir)
            else:
                unbalanced_directories.append({
                    'directory': images_dir,
                    'expected': expected_samples_per_dir,
                    'actual': count
                })
    
    total_directories = len(config.freq_ranges) * len(scenarios)
    
    summary = {
        'total_directories': total_directories,
        'balanced_directories': len(balanced_directories),
        'unbalanced_directories': len(unbalanced_directories),
        'missing_directories': len(missing_directories),
        'expected_samples_per_dir': expected_samples_per_dir
    }
    
    logger.info("Dataset verification complete:")
    logger.info(f"Total directories: {total_directories}")
    logger.info(f"Balanced: {len(balanced_directories)}")
    logger.info(f"Unbalanced: {len(unbalanced_directories)}")
    logger.info(f"Missing: {len(missing_directories)}")
    
    if unbalanced_directories:
        logger.warning("Unbalanced directories:")
        for item in unbalanced_directories[:5]:  # Show first 5
            logger.warning(
                f"  {item['directory']}: expected {item['expected']}, "
                f"found {item['actual']}"
            )
    
    if missing_directories:
        logger.warning("Missing directories:")
        for dir_path in missing_directories[:5]:  # Show first 5
            logger.warning(f"  {dir_path}")
    
    return {
        'total_directories': total_directories,
        'balanced_directories': balanced_directories,
        'unbalanced_directories': unbalanced_directories,
        'missing_directories': missing_directories,
        'directory_counts': directory_counts,
        'summary': summary
    }


def main() -> None:
    """
    Main entry point for synthetic data generation.
    
    Why: Provides a standard entry point for command-line execution.
    This function loads configuration and executes balanced dataset generation
    across all frequency ranges and scenarios with hierarchical directory structure.
    Ensures equal number of samples per directory for balanced training data.
    
    What: Creates a SyntheticDataConfig object (which can be overridden by
    environment variables), accepts command-line arguments for number of samples
    per directory, and calls generate_balanced_dataset() to create samples
    systematically for all (freq_range, scenario) combinations. Verifies dataset
    balance at the end. The order is fixed, but signal parameters are randomized.
    
    Raises:
        ConfigurationError: If configuration is invalid.
        SignalGenerationError: If sample generation fails.
    """
    import argparse
    import warnings
    # Suppress RuntimeWarning about module import in multiprocessing
    # This warning occurs when ProcessPoolExecutor imports modules in worker processes
    warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')
    
    parser = argparse.ArgumentParser(
        description='Generate balanced synthetic data dataset with equal samples per directory'
    )
    parser.add_argument(
        '--samples_per_directory',
        type=int,
        default=5,
        help='Number of samples to generate per directory (default: 5)'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help='Base output directory (default: uses config.output_dir)'
    )
    parser.add_argument(
        '--max_workers',
        type=int,
        default=None,
        help='Maximum number of parallel workers (default: auto - CPU count)'
    )
    args = parser.parse_args()
    
    config = SyntheticDataConfig()
    logger.info("Synthetic Data Generation - Balanced Dataset")
    logger.info(f"Configuration: fs={config.fs}, duration={config.duration}")
    logger.info(f"Samples per directory: {args.samples_per_directory}")
    
    # Generate balanced dataset
    stats = generate_balanced_dataset(
        samples_per_directory=args.samples_per_directory,
        config=config,
        base_output_dir=args.output_dir,
        max_workers=args.max_workers
    )
    
    # Verify dataset balance
    if args.output_dir is None:
        output_dir = config.output_dir
    else:
        output_dir = args.output_dir
    
    logger.info("Verifying dataset balance...")
    verification = verify_dataset_balance(
        base_output_dir=output_dir,
        expected_samples_per_dir=args.samples_per_directory,
        config=config
    )
    
    # Final summary
    logger.info("=" * 60)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Generation: {stats['total_samples_success']}/{stats['total_samples_expected']} samples")
    logger.info(f"Verification: {verification['summary']['balanced_directories']}/{verification['summary']['total_directories']} directories balanced")
    if verification['summary']['unbalanced_directories'] > 0:
        logger.warning(f"WARNING: {verification['summary']['unbalanced_directories']} directories are unbalanced!")
    if verification['summary']['missing_directories'] > 0:
        logger.warning(f"WARNING: {verification['summary']['missing_directories']} directories are missing!")


if __name__ == "__main__":
    main()
