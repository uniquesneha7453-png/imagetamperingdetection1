"""
Prediction & Inference Module

Provides a clean, reusable function to detect image tampering using Error Level Analysis (ELA)
and the trained Keras model.

Pipeline:
  1. Validates that the image file exists and is readable.
  2. Ensures the trained model (outputs/tampering_model.keras) is loaded.
  3. Preprocesses the image:
       Original Image -> ELA -> 224x224 RGB -> Float32 -> Normalization [0.0, 1.0]
  4. Runs inference through the model.
  5. Returns a structured dictionary:
       - label: "REAL" or "TAMPERED"
       - confidence: float (0.0 to 1.0)
       - probability: raw sigmoid output probability (0.0 to 1.0)
       - image_path: resolved image file path
"""

import sys
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import keras

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import prepare_image_for_model

DEFAULT_MODEL_PATH = PROJECT_ROOT / "outputs" / "tampering_model.keras"

# Cached model instance for fast repeated predictions
_LOADED_MODEL = None
_LOADED_MODEL_PATH = None


def load_model_if_exists(model_path=DEFAULT_MODEL_PATH):
    """
    Loads and caches the trained Keras model.

    Raises:
        FileNotFoundError: If the model file does not exist.
    """
    global _LOADED_MODEL, _LOADED_MODEL_PATH
    m_path = Path(model_path).resolve()

    if not m_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at '{m_path}'.\n"
            "The model has not been trained yet. Please train the model first by:\n"
            "  1. Placing training images in 'dataset/real/' and 'dataset/tampered/'\n"
            "  2. Running: python src/train.py"
        )

    if _LOADED_MODEL is None or _LOADED_MODEL_PATH != str(m_path):
        _LOADED_MODEL = keras.models.load_model(str(m_path))
        _LOADED_MODEL_PATH = str(m_path)

    return _LOADED_MODEL


def predict_tampering(image_path, model_path=DEFAULT_MODEL_PATH):
    """
    Predict whether an input image is REAL or TAMPERED.

    Integration Function for Teammates:
        from src.predict import predict_tampering
        result = predict_tampering("path/to/image.jpg")

    Args:
        image_path (str | Path): Path to the input image file.
        model_path (str | Path): Path to the trained .keras model file.

    Returns:
        dict:
            - label (str): "REAL" or "TAMPERED"
            - confidence (float): Decision confidence between 0.0 and 1.0
            - probability (float): Raw sigmoid output probability (P(TAMPERED))
            - image_path (str): The resolved image path

    Raises:
        FileNotFoundError: If the input image file or model file does not exist.
        ValueError: If the file is not a valid or readable image.
    """
    img_path = Path(image_path).resolve()

    # 1. Validate that the image file exists
    if not img_path.exists():
        raise FileNotFoundError(f"Input image not found: {img_path}")
    if not img_path.is_file():
        raise FileNotFoundError(f"Specified path is not a file: {img_path}")

    # 2. Validate that the image file is readable and uncorrupted
    try:
        with Image.open(img_path) as test_img:
            test_img.verify()
    except Exception as err:
        raise ValueError(f"Corrupt or unsupported image file '{img_path}': {err}")

    # 3. Load trained model (raises FileNotFoundError if model doesn't exist)
    model = load_model_if_exists(model_path)

    # 4. Preprocess: Raw image -> ELA -> 224x224 RGB -> [0, 1] float32 tensor
    input_tensor, _ = prepare_image_for_model(img_path, add_batch_dim=True)

    # 5. Run inference
    raw_pred = model.predict(input_tensor, verbose=0)
    prob_tampered = float(raw_pred[0][0])

    # 6. Binary classification:
    # Class 0 = REAL
    # Class 1 = TAMPERED
    if prob_tampered >= 0.5:
        label = "TAMPERED"
        confidence = prob_tampered
    else:
        label = "REAL"
        confidence = 1.0 - prob_tampered

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "probability": round(prob_tampered, 4),
        "image_path": str(img_path),
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_img = sys.argv[1]
        try:
            result = predict_tampering(target_img)
            print("\n" + "=" * 50)
            print("  TAMPERING DETECTION RESULT")
            print("=" * 50)
            print(f"Image:       {result['image_path']}")
            print(f"Prediction:  {result['label']}")
            print(f"Confidence:  {result['confidence'] * 100:.2f}%")
            print(f"Probability: {result['probability']:.4f}")
            print("=" * 50)
        except (FileNotFoundError, ValueError) as err:
            print(f"\n[Error] {err}")
            sys.exit(1)
        except Exception as err:
            print(f"\n[Unexpected Error] {err}")
            sys.exit(1)
    else:
        print("Usage: python src/predict.py <path_to_image>")
