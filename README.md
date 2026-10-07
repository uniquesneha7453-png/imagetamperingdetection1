# Image Tampering Detection: Real vs Edited

### Detecting Image Manipulation Using Error Level Analysis and Machine Learning

> **PIXELS → EVIDENCE → VERDICT**

## Overview

Image tampering involves modifying an image using techniques such as
copy-paste, splicing, or retouching.

This project aims to develop a system that detects whether an input image is
likely to be **Real** or **Tampered**.

The system uses **Error Level Analysis (ELA)** to identify regions that may
show inconsistent compression patterns and Machine Learning for classification.

---

## Problem Statement

Manipulated images can reduce trust in digital content and create challenges
in areas such as:

- Digital evidence
- Cybersecurity
- Misinformation detection
- Online media verification

The goal of this project is to develop an image-forensics system that can
assist in identifying potentially manipulated images.

---

## Proposed Solution

The system follows this general pipeline:

```text
Input Image
     ↓
Preprocessing
     ↓
Error Level Analysis (ELA)
     ↓
ELA Heatmap
     ↓
Feature Extraction
     ↓
Machine Learning Classifier
     ↓
REAL / TAMPERED
```

---

## Error Level Analysis (ELA)

Error Level Analysis compares an image with a recompressed version of the
same image.

The basic process involves:

1. Taking the input image
2. Recompressing it as a JPEG
3. Comparing the original and recompressed images
4. Calculating pixel-level differences
5. Generating an ELA heatmap

Unusual compression differences may indicate possible image manipulation.

**Note:** ELA is an indicator and not absolute proof that an image has been
tampered with.

---

## Machine Learning

The ELA representation is used to obtain features from the image.

These features are then used by a Machine Learning classifier to predict
whether the image is:

- **REAL**
- **TAMPERED**

---

## Technologies Used

- Python
- OpenCV
- Pillow
- scikit-learn
- Google Colab

---

## Evaluation

The system can be evaluated using:

- Accuracy
- Confusion Matrix

Final results will be added after the model is trained and evaluated.

---

## Demo

The intended demonstration follows these steps:

```text
Upload Image
     ↓
Image Processing
     ↓
ELA Generation
     ↓
ELA Heatmap
     ↓
ML Prediction
     ↓
REAL / TAMPERED
```

---

## Limitations

- ELA depends on JPEG compression.
- Resizing and screenshots can affect ELA patterns.
- ELA alone cannot prove that an image is fake.
- Performance depends on the quality and diversity of the dataset.

---

## Future Scope

- Larger and more diverse datasets
- Advanced image-forensics techniques
- Deep Learning-based detection
- Support for newer image manipulation techniques
- More robust testing across different image formats

---

## Cybersecurity Relevance

Image forgery detection can support cybersecurity and digital forensics by
helping identify potentially manipulated visual information.

This project combines image processing and Machine Learning to assist in
evaluating the authenticity of digital images.

---

## Disclaimer

This project is an educational and research-oriented prototype. The prediction
should not be treated as definitive proof of image authenticity.
