"""
Preprocessing Module

Transforms an ELA image (or original image path) into a normalized NumPy array
ready for input into a Keras deep learning model:
  1. ELA extraction (if given a raw image path)
  2. Resize to exactly 224x224
  3. Ensure RGB format (3 channels)
  4. Cast pixel values to float32
  5. Normalize pixel values to the range [0.0, 1.0]
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

# Ensure project root is in sys.path for direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ela import generate_ela_image

# Standard input dimensions expected by the model
TARGET_SIZE = (224, 224)


def preprocess_ela_image(ela_image_or_path, target_size=TARGET_SIZE, add_batch_dim=False):
    """
    Takes an ELA image (as a PIL Image or file path) and prepares it for model input.

    Steps:
      - Resize to target_size (224x224)
      - Convert to RGB
      - Convert pixel values to float32
      - Normalize values to [0.0, 1.0]

    Args:
        ela_image_or_path (str | Path | Image.Image): ELA PIL Image or path to an ELA image file.
        target_size (tuple): Target size as (width, height). Defaults to (224, 224).
        add_batch_dim (bool): If True, adds a leading batch dimension -> shape (1, 224, 224, 3).

    Returns:
        np.ndarray: Preprocessed NumPy array with shape (224, 224, 3) or (1, 224, 224, 3),
                    dtype float32, normalized to [0.0, 1.0].
    """
    # 1. Open the image if a path is provided
    if isinstance(ela_image_or_path, (str, Path)):
        img = Image.open(str(ela_image_or_path))
    elif isinstance(ela_image_or_path, Image.Image):
        img = ela_image_or_path
    else:
        raise TypeError("Input must be a file path (str/Path) or a PIL Image object.")

    # 2. Ensure the image is in RGB format (3 channels)
    img_rgb = img.convert("RGB")

    # 3. Resize to exactly 224x224
    img_resized = img_rgb.resize(target_size, Image.Resampling.LANCZOS)

    # 4. Convert pixel values to float32 NumPy array
    img_array = np.array(img_resized, dtype=np.float32)

    # 5. Normalize pixel values to [0.0, 1.0]
    img_normalized = img_array / 255.0

    # 6. Optionally add batch dimension for single-image model prediction
    if add_batch_dim:
        img_normalized = np.expand_dims(img_normalized, axis=0)

    return img_normalized


def prepare_image_for_model(raw_image_path, target_size=TARGET_SIZE, quality=90, scale=15, add_batch_dim=True):
    """
    End-to-end preprocessing helper:
      Raw image path -> ELA generation -> 224x224 RGB -> [0, 1] normalization -> Model tensor.

    Args:
        raw_image_path (str | Path): Path to the original raw image.
        target_size (tuple): Target image dimensions (default: 224x224).
        quality (int): JPEG quality level for ELA recompression (default: 90).
        scale (int | float): Brightness enhancement factor for ELA (default: 15).
        add_batch_dim (bool): If True, returns tensor with shape (1, 224, 224, 3).

    Returns:
        tuple[np.ndarray, Image.Image]:
            - input_tensor: Normalized float32 NumPy array ready for model input.
            - ela_image: Intermediate PIL Image of the ELA result (useful for visualization).
    """
    # Generate ELA image
    ela_image = generate_ela_image(raw_image_path, quality=quality, scale=scale)

    # Preprocess into normalized float32 array
    input_tensor = preprocess_ela_image(ela_image, target_size=target_size, add_batch_dim=add_batch_dim)

    return input_tensor, ela_image
