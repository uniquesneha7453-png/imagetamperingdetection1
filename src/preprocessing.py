from PIL import Image
from pathlib import Path


def prepare_ela_image(
    ela_path,
    output_path,
    size=(224, 224)
):

    image = Image.open(ela_path)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize(size)

    # Create output directory
    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the processed image
    image.save(output_path)

    return output_path


if __name__ == "__main__":

    input_ela = "outputs/test_ela.png"
    output_ela = "outputs/test_ela_ready.png"

    prepare_ela_image(
        input_ela,
        output_ela
    )

    print("ELA image prepared successfully!")
    print("Output:", output_ela)