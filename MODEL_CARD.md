Model Card

Model Overview

The Image Tampering Detection model is a binary image-classification model designed to identify whether an input image is likely to be authentic or manipulated.

The model operates on an Error Level Analysis (ELA) representation of the input image.

Intended Use

The model is intended for:

- Educational projects
- Image-forensics research
- Demonstration of ELA-based tampering detection
- Experimental analysis of potentially manipulated images

The output should be considered an automated indication rather than definitive proof of image authenticity.

Classification Classes

The model produces two classes:

| Class | Meaning |
|---|---|
| REAL | Image classified as authentic |
| TAMPERED | Image classified as potentially manipulated |

Input Processing

Before inference, an input image passes through the following processing pipeline:

1. Image validation
2. RGB conversion
3. JPEG recompression
4. Error Level Analysis
5. ELA enhancement
6. Resize to 224 × 224 pixels
7. Conversion to `float32`
8. Normalization to the range 0.0–1.0

ELA Configuration

The current implementation uses:

- JPEG quality: 90
- Enhancement scale: 15
- Input resolution: 224 × 224
- Color channels: RGB

Prediction

The model produces a probability corresponding to the TAMPERED class.

The prediction threshold is:

```text
Probability >= 0.5 → TAMPERED
Probability < 0.5  → REAL
