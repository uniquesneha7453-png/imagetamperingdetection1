"""
Error Level Analysis (ELA) Module

This module generates ELA images from original input images.
ELA works by resaving an image at a known JPEG compression rate (e.g. 90%)
and calculating the pixel difference between the original and recompressed versions.
Because authentic and manipulated regions compress differently, tampering artifacts
stand out as higher error levels.
"""

import io
from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance


def generate_ela_image(image_input, output_path=None, quality=90, scale=15):
    """
    Generate an Error Level Analysis (ELA) image.

    Args:
        image_input (str | Path | Image.Image): Path to the image or an open PIL Image.
        output_path (str | Path | None): Optional file path to save the generated ELA image.
        quality (int): JPEG quality level used for recompression (default: 90).
        scale (int | float): Scale factor to enhance the contrast of the difference (default: 15).

    Returns:
        Image.Image: The resulting ELA image as a PIL Image in RGB mode.
    """
    # 1. Load the original image
    if isinstance(image_input, (str, Path)):
        orig_image = Image.open(str(image_input))
    elif isinstance(image_input, Image.Image):
        orig_image = image_input
    else:
        raise TypeError("image_input must be a file path (str/Path) or a PIL Image object.")

    # 2. Safely convert to RGB (handles RGBA, grayscale 'L', palette 'P', etc.)
    # This prevents errors when saving as JPEG (which does not support alpha channels)
    orig_rgb = orig_image.convert("RGB")

    # 3. Recompress the image in memory at the given JPEG quality
    buffer = io.BytesIO()
    orig_rgb.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    recompressed_image = Image.open(buffer)

    # 4. Calculate the absolute pixel-by-pixel difference
    ela_diff = ImageChops.difference(orig_rgb, recompressed_image)

    # 5. Amplify the difference so subtle error levels become visible
    enhanced_ela = ImageEnhance.Brightness(ela_diff).enhance(scale)

    # 6. Save to disk if an output path was specified
    if output_path is not None:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        enhanced_ela.save(str(out_p))

    return enhanced_ela


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        save_file = sys.argv[2] if len(sys.argv) > 2 else "ela_result.png"
        print(f"Generating ELA for: {input_file}")
        result_img = generate_ela_image(input_file, output_path=save_file)
        print(f"ELA image successfully saved to: {save_file}")
    else:
        print("Usage: python src/ela.py <input_image_path> [output_image_path]")
