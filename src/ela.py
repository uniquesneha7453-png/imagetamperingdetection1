from PIL import Image, ImageChops, ImageEnhance
from io import BytesIO
from pathlib import Path


def load_image(image_path):
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError("Image not found.")

    try:
        image = Image.open(path)
        image.load()
        return image.convert("RGB")
    except Exception:
        raise ValueError("Unable to read the image.")


def generate_ela(image_path, output_path, quality=90):

    original = load_image(image_path)

    # Compress the image as JPEG
    buffer = BytesIO()
    original.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    compressed = Image.open(buffer).convert("RGB")

    # Calculate pixel differences
    difference = ImageChops.difference(
        original,
        compressed
    )

    # Find maximum difference
    extrema = difference.getextrema()

    max_difference = max(
        value for minimum, value in extrema
    )

    if max_difference == 0:
        max_difference = 1

    # Increase brightness of differences
    scale = 255 / max_difference

    ela_image = ImageEnhance.Brightness(
        difference
    ).enhance(scale)

    # Create output folder
    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ela_image.save(output_path)

    return output_path


if __name__ == "__main__":

    input_image = "input_images/test.jpg"
    output_image = "outputs/test_ela.png"

    try:
        generate_ela(
            input_image,
            output_image
        )

        print("ELA image created successfully!")
        print("Output:", output_image)

    except Exception as error:
        print("Error:", error)