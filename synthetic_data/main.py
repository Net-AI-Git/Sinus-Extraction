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
from typing import Optional, Tuple, List, Dict, Any
import numpy as np
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

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


def _setup_hierarchical_directories(
    base_output_dir: str,
    freq_range: Tuple[float, float],
    scenario_name: str
) -> Tuple[str, str]:
    """
    Create hierarchical output directories for frequency range and scenario.
    
    Why: Organizes output data hierarchically by frequency range and signal
    scenario, enabling organized dataset structure and easy filtering.
    
    What: Creates directory structure: base_output_dir/freq_X_Y/scenario_name/images/
    and masks/. Uses exist_ok=True to avoid errors if directories already exist.
    
    Args:
        base_output_dir: Base output directory path.
        freq_range: Frequency range tuple (fmin, fmax).
        scenario_name: Signal scenario name.
    
    Returns:
        Tuple[str, str]: A tuple containing (images_dir, masks_dir) paths.
    
    Raises:
        OSError: If directories cannot be created.
    """
    config = SyntheticDataConfig()
    freq_dir_name = config.get_freq_range_dir_name(freq_range[0], freq_range[1])
    scenario_dir = os.path.join(base_output_dir, freq_dir_name, scenario_name)
    images_dir = os.path.join(scenario_dir, 'images')
    masks_dir = os.path.join(scenario_dir, 'masks')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    return images_dir, masks_dir


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
    
    images_dir, masks_dir = _setup_hierarchical_directories(
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
        base_name = f'sample_{unique_id}.jpg'
        image_filename = os.path.join(images_dir, base_name)
        mask_filename = os.path.join(masks_dir, base_name)
        save_image(sample.stft, image_filename, config, cmap='viridis', save_raw=True)
        save_image(
            sample.binary_mask,
            mask_filename,
            config,
            cmap='gray',
            title='Binary Mask',
            save_raw=True
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
) -> Tuple[str, str, int]:
    """
    Generate and save a single sample (for parallel processing).
    
    Why: This function is designed to be picklable for ProcessPoolExecutor.
    It receives all necessary parameters as a dictionary and creates a new
    RNG instance to avoid pickling issues.
    
    What: Creates a new RNG from the provided seed, generates a sample with
    the specified parameters, saves both STFT and mask images, and returns
    status information.
    
    Args:
        task_params: Dictionary containing all parameters needed for sample
            generation: seed, config_dict, n_components, snr_db, tf_sigma,
            signal_scenario, freq_range, images_dir, masks_dir, sample_index,
            total_samples, combination_info.
    
    Returns:
        Tuple[str, str, int]: (status, message, sample_index)
    """
    # Import here to avoid pickling issues
    import os
    import uuid
    import numpy as np
    from synthetic_data.config import SyntheticDataConfig
    from synthetic_data.sample_generator import generate_sample
    from synthetic_data.visualization import save_image
    
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
        base_name = f'sample_{unique_id}.jpg'
        image_filename = os.path.join(task_params['images_dir'], base_name)
        mask_filename = os.path.join(task_params['masks_dir'], base_name)
        
        save_image(
            sample.stft,
            image_filename,
            config,
            cmap='viridis',
            save_raw=True
        )
        save_image(
            sample.binary_mask,
            mask_filename,
            config,
            cmap='gray',
            title='Binary Mask',
            save_raw=True
        )
        
        return (
            'success',
            f"Sample {task_params['sample_index']}/{task_params['total_samples']}: "
            f"{task_params['combination_info']} - {base_name}",
            task_params['sample_index']
        )
    except Exception as e:
        return (
            'error',
            f"Error generating sample {task_params['sample_index']}: {str(e)}",
            task_params['sample_index']
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
            images_dir, masks_dir = _setup_hierarchical_directories(
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
            status, message, sample_idx = future.result()
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


def main() -> None:
    """
    Main entry point for synthetic data generation.
    
    Why: Provides a standard entry point for command-line execution.
    This function loads configuration and executes systematic sample generation
    across all frequency ranges and scenarios with hierarchical directory structure.
    
    What: Creates a SyntheticDataConfig object (which can be overridden by
    environment variables), accepts command-line arguments for number of samples
    per combination, and calls generate_diverse_samples() to create samples
    systematically for all (freq_range, scenario) combinations. The order is
    fixed, but signal parameters are randomized.
    
    Raises:
        ConfigurationError: If configuration is invalid.
        SignalGenerationError: If sample generation fails.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate synthetic data samples systematically across all frequency ranges and scenarios'
    )
    parser.add_argument(
        '--n_samples',
        type=int,
        default=3,
        help='Number of samples to generate per (freq_range, scenario) combination (default: 3)'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help='Base output directory (default: uses config.output_dir)'
    )
    args = parser.parse_args()
    
    config = SyntheticDataConfig()
    logger.info("Synthetic Data Generation")
    logger.info(f"Configuration: fs={config.fs}, duration={config.duration}")
    
    generate_diverse_samples(
        n_samples=args.n_samples,
        config=config,
        base_output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
