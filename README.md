# Sinus Extraction - Image Segmentation

Jupyter notebook for implementing a Segmentation model to detect sinuses in images.

## Usage in Google Colab

### Load the notebook directly from GitHub:

1. Open [Google Colab](https://colab.research.google.com/)
2. Click **File** → **Open notebook**
3. Select the **GitHub** tab
4. Paste the repository URL:
   ```
   https://github.com/Net-AI-Git/Sinus-Extraction
   ```
5. Select the notebook: `Segmentation_code_templates/ImageSegmentation_template.ipynb`
6. Click **Open**

### Direct link to Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Net-AI-Git/Sinus-Extraction/blob/main/Segmentation_code_templates/ImageSegmentation_template.ipynb)

Or copy this link:
```
https://colab.research.google.com/github/Net-AI-Git/Sinus-Extraction/blob/main/Segmentation_code_templates/ImageSegmentation_template.ipynb
```

## Updating the Notebook

When you make changes to the notebook and push them to GitHub:

1. In Colab, click **File** → **Revert to last saved version** (if you have unsaved changes)
2. Or refresh the page (F5) to load the new version from GitHub

## Requirements

The notebook includes all the commands to install the required packages. Simply run the cells in order.

## Project Structure

```
Sinus-Extraction/
└── Segmentation_code_templates/
    └── ImageSegmentation_template.ipynb
```

## Features

- Ready to use in Colab with GPU support
- All paths are configured for Colab environment (`/content/`)
- Includes UNet model configuration with ResNet18 backbone
- Comprehensive logging system with HTML color formatting
- Type-safe configuration using dataclasses
- Custom exception handling for configuration errors

## Notes

- The notebook is optimized for grayscale image segmentation
- Training from scratch (no pre-trained weights) for grayscale images
- Includes data augmentation, custom dataset, and training pipeline

