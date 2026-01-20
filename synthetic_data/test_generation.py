"""
Quick test script for synthetic data generation.

This script generates a few samples and displays them for visual inspection.
"""

import sys
import os
import json

# #region agent log
log_path = r"c:\Users\NETANIT\Desktop\work\Sinus-Extraction\.cursor\debug.log"
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"test_generation.py:15","message":"Checking sys.path","data":{"cwd":os.getcwd(),"script_dir":os.path.dirname(__file__),"parent_dir":parent_dir,"parent_in_path":parent_dir in sys.path,"sys_path":sys.path[:5]},"timestamp":int(__import__('time').time()*1000)}) + "\n")
except: pass
# #endregion

# Add parent directory to path if not present (hypothesis A fix)
if parent_dir not in sys.path:
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"test_generation.py:22","message":"Adding parent to sys.path","data":{"parent_dir":parent_dir},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    sys.path.insert(0, parent_dir)

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"test_generation.py:20","message":"Attempting import","data":{"importing":"synthetic_data"},"timestamp":int(__import__('time').time()*1000)}) + "\n")
except: pass
# #endregion

try:
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"test_generation.py:32","message":"Testing __init__ import","data":{},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    import synthetic_data
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"test_generation.py:38","message":"Module imported, checking attributes","data":{"has_config":"SyntheticDataConfig" in dir(synthetic_data)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    from synthetic_data import (
        SyntheticDataConfig,
        generate_and_display_pairs_convenience,
        save_image,
    )
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"test_generation.py:48","message":"Import successful","data":{},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
except Exception as e:
    # #region agent log
    try:
        import traceback
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"test_generation.py:54","message":"Import failed","data":{"error":str(e),"error_type":type(e).__name__,"traceback":traceback.format_exc()},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    raise

# #region agent log
try:
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"test_generation.py:40","message":"Checking setup_logger import","data":{},"timestamp":int(__import__('time').time()*1000)}) + "\n")
except: pass
# #endregion

from synthetic_data.logger_setup import setup_logger

# Setup logger
logger = setup_logger('synthetic_data')

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate and save synthetic data samples')
    parser.add_argument(
        '--n_pairs',
        type=int,
        default=5,
        help='Number of sample pairs to generate (default: 5)'
    )
    args = parser.parse_args()
    
    logger.info(f"Generating and displaying {args.n_pairs} sample pairs...")
    
    # Create config
    config = SyntheticDataConfig()
    
    # Generate and display pairs
    samples = generate_and_display_pairs_convenience(n_pairs=args.n_pairs, config=config)
    
    # Save images
    logger.info("Saving images...")
    images_dir = os.path.join(config.output_dir, 'images')
    masks_dir = os.path.join(config.output_dir, 'masks')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)
    
    # #region agent log
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"test_generation.py:95","message":"Saving samples to disk","data":{"images_dir":images_dir,"masks_dir":masks_dir,"abs_images":os.path.abspath(images_dir),"abs_masks":os.path.abspath(masks_dir),"num_samples":len(samples)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
    except: pass
    # #endregion
    
    for i, sample in enumerate(samples):
        base_name = f'sample_{i:06d}.jpg'
        image_filename = os.path.join(images_dir, base_name)
        mask_filename = os.path.join(masks_dir, base_name)
        # #region agent log
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"test_generation.py:103","message":"Saving sample","data":{"index":i,"image_filename":image_filename,"mask_filename":mask_filename},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
        save_image(sample.stft, image_filename, config, cmap='viridis', save_raw=True)
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
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"F","location":"test_generation.py:115","message":"After saving sample","data":{"index":i,"image_exists":os.path.exists(image_filename),"mask_exists":os.path.exists(mask_filename)},"timestamp":int(__import__('time').time()*1000)}) + "\n")
        except: pass
        # #endregion
    
    logger.info(f"Generated {len(samples)} samples successfully!")
    logger.info(f"Images saved to: {images_dir}")
    logger.info(f"Masks saved to: {masks_dir}")
