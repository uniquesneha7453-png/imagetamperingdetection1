"""
Preprocessing Module

Transforms an ELA image (or original image path) into a normalized NumPy array
ready for input into a Keras deep learning model.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ela import generate_ela_image

TARGET_SIZE = (224, 224)


def preprocess_ela_image(ela_image_or_path, target_size=TARGET_SIZE, add_batch_dim=False):
    if isinstance(ela_image_or_path, (str, Path)):
        img = Image.open(str(ela_image_or_path))
    elif isinstance(ela_image_or_path, Image.Image):
        img = ela_image_or_path
    else:
        raise TypeError("Input must be a file path (str/Path) or a PIL Image object.")

    img_rgb = img.convert("RGB")
    img_resized = img_rgb.resize(target_size, Image.Resampling.LANCZOS)

    img_array = np.array(img_resized, dtype=np.float32)
    img_normalized = img_array / 255.0

    if add_batch_dim:
        img_normalized = np.expand_dims(img_normalized, axis=0)

    return img_normalized


def prepare_image_for_model(
    raw_image_path,
    target_size=TARGET_SIZE,
    quality=90,
    scale=15,
    add_batch_dim=True
):
    ela_image = generate_ela_image(
        raw_image_path,
        quality=quality,
        scale=scale
    )

    input_tensor = preprocess_ela_image(
        ela_image,
        target_size=target_size,
        add_batch_dim=add_batch_dim
    )

    return input_tensor, ela_image