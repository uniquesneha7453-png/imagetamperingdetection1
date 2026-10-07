# Image Tampering Detection (Hackathon Project)

An end-to-end Machine Learning pipeline to detect digital image forgery and manipulation using **Error Level Analysis (ELA)** and a lightweight **Deep Learning CNN Classifier**.

---

## 🔍 Pipeline Architecture

```text
Original Image
     │
     ▼
[ ELA Preprocessing ] (JPEG recompression difference via Pillow)
     │
     ▼
[ Resize & Format ]   (224x224 RGB image, 3 channels)
     │
     ▼
[ Normalization ]     (Float32 conversion, pixel values scaled to [0.0, 1.0])
     │
     ▼
[ ML Model ]          (Lightweight MobileNetV2-based CNN classifier)
     │
     ▼
[ Binary Decision ]   (0 = REAL, 1 = TAMPERED + Confidence Score)
```

---

## 📁 Project Structure

```text
Image-Tampering-Hackothon/
│
├── dataset/                    # Future dataset folder (created when data is available)
│   ├── real/                   # Authentic, unedited images (Class 0)
│   └── tampered/               # Manipulated/forged images (Class 1)
│
├── input_images/               # Folder for test/demo images
├── outputs/                    # Saved models and exported evaluation artifacts
│   └── tampering_model.keras   # Generated upon training
│
├── src/
│   ├── ela.py                  # Error Level Analysis generation using Pillow
│   ├── preprocessing.py        # 224x224 RGB resizing, float32 conversion & [0, 1] normalization
│   ├── model.py                # Reusable lightweight MobileNetV2 Keras model
│   ├── train.py                # Dataset loading, train/val split & model training routine
│   └── predict.py              # Reusable inference function & CLI tool
│
├── tests/                      # Unit and integration test scripts
└── README.md                   # Project documentation and guide
```

---

## ⚙️ Environment & Dependencies

- **Python**: 3.13+
- **TensorFlow**: 2.20.0
- **Keras**: 3.13.2
- **Pillow**: 12.0.0
- **NumPy**: Included with TensorFlow / Keras

> **Note:** The pipeline is designed to work completely **offline** on CPU without requiring OpenCV (`cv2`) or PyTorch (`torch`).

---

## 🚀 How to Use

### 1. Dataset Setup (Future Step)

When you receive or download your dataset (e.g., CASIA 2.0 or custom tampering dataset), organize your images as follows:

```text
dataset/
├── real/
│   ├── photo_001.jpg
│   └── photo_002.png
└── tampered/
    ├── fake_001.jpg
    └── fake_002.png
```

Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff`, `.webp`.

---

### 2. Training the Model

Once images are placed in `dataset/`, train the model with a single command:

```powershell
python src/train.py
```

- Loads images batch-by-batch using `keras.utils.PyDataset` to prevent high memory usage.
- Computes ELA and normalizes each image to `(224, 224, 3)`.
- Splits data into 80% training and 20% validation.
- Automatically saves the best model checkpoint to `outputs/tampering_model.keras`.
- Displays training loss, accuracy, precision, and recall metrics upon completion.

---

### 3. Running Predictions (Inference)

#### Via Command Line:
```powershell
python src/predict.py path/to/sample_image.jpg
```

Output format:
```text
==================================================
  TAMPERING DETECTION RESULT
==================================================
Image:      path/to/sample_image.jpg
Prediction: TAMPERED
Confidence: 94.20%
==================================================
```

#### Integration for Teammates (UI / Backend API):
Teammates can directly import and invoke `predict_tampering`:

```python
from src.predict import predict_tampering

result = predict_tampering("path/to/image.jpg")
print(result)
# Returns:
# {
#     "label": "REAL" or "TAMPERED",
#     "confidence": 0.942,
#     "raw_probability": 0.942,
#     "image_path": "..."
# }
```

If the model has not been trained yet, it cleanly raises a descriptive `FileNotFoundError` explaining how to train it.

---

### 4. Standalone ELA Extraction

To inspect or visualize the ELA representation of any image:

```powershell
python src/ela.py input_images/test.jpg outputs/ela_preview.png
```
