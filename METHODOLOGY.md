Methodology
 1. Introduction

The Image Tampering Detection system uses Error Level Analysis (ELA) combined with a trained machine learning model to classify an input image as either REAL or TAMPERED.

The methodology is divided into four main stages:

1. Image validation
2. Error Level Analysis
3. Image preprocessing
4. Machine learning inference

---

 2. Overall Workflow

The complete processing pipeline is:

```text
Input Image
     ↓
Image Validation
     ↓
Error Level Analysis (ELA)
     ↓
224 × 224 RGB Image
     ↓
Pixel Normalization
     ↓
Trained Keras Model
     ↓
Tampering Probability
     ↓
REAL / TAMPERED


---

3. Image Validation

Before performing detection, the system verifies that the input image is valid and readable.

The following checks are performed:

The specified image path exists.

The path points to a file.

The image can be opened successfully.

The image is not corrupted or unsupported.


If the image cannot be read, an appropriate error is returned instead of passing the invalid input to the model.


---

4. Error Level Analysis

Error Level Analysis (ELA) is used to generate a representation of compression differences within an image.

The input image is first converted to RGB format and then recompressed using JPEG compression.

The original image and the recompressed image are compared pixel by pixel. The differences are enhanced to make variations in compression levels more visible.

The ELA implementation uses:

Parameter	Value

JPEG Quality	90
Enhancement Scale	15


Regions with unusual compression differences may provide useful information for identifying possible image manipulation.

ELA is treated as an indicator of possible manipulation and not as absolute proof that an image has been edited.


---

5. Image Preprocessing

After ELA generation, the resulting image is prepared for model inference.

The preprocessing pipeline consists of:

1. Converting the image to RGB.


2. Resizing the image to 224 × 224 pixels.


3. Converting the image into a NumPy array.


4. Converting pixel values to float32.


5. Normalizing pixel values from the range 0–255 to 0.0–1.0.


6. Adding a batch dimension before model inference.



The final model input has the shape:

(1, 224, 224, 3)


---

6. Machine Learning Inference

The processed ELA representation is passed to the trained Keras model.

The trained model is loaded from:

outputs/tampering_model.keras

The model produces a probability representing the likelihood that the image belongs to the TAMPERED class.

The classification threshold used by the prediction module is 0.5.

Probability ≥ 0.5  →  TAMPERED
Probability < 0.5  →  REAL


---

7. Prediction Output

The prediction module returns a structured result containing:

Output	Description

label	Predicted class: REAL or TAMPERED
confidence	Confidence associated with the predicted class
probability	Raw probability of the TAMPERED class
image_path	Resolved path of the input image


For example:

Prediction: TAMPERED
Confidence: 0.92
Probability: 0.92

The values shown above are an example of the output format and are not intended to represent measured model performance.


---

8. Project Modules

The detection system separates different responsibilities into individual modules.

src/ela.py

Responsible for generating the Error Level Analysis representation.

src/preprocessing.py

Responsible for converting the ELA image into the format required by the machine learning model.

src/predict.py

Responsible for:

Loading the trained model

Validating input images

Running preprocessing

Performing model inference

Returning the prediction result


src/train.py

Responsible for the model training process.


---

9. End-to-End Process

The complete process can be summarized as follows:

User Input
    ↓
Validate Image
    ↓
Generate ELA
    ↓
Resize to 224 × 224
    ↓
Convert to RGB
    ↓
Normalize to [0, 1]
    ↓
Load Trained Keras Model
    ↓
Run Prediction
    ↓
Calculate Tampering Probability
    ↓
Apply 0.5 Classification Threshold
    ↓
REAL / TAMPERED


---

10. Error Handling

The system includes validation and error handling for common problems.

Examples include:

Missing input image

Invalid image path

Corrupted image

Unsupported image

Missing trained model

Unexpected inference errors


This prevents invalid inputs from being processed silently.


---

11. Reusability

The prediction functionality is implemented as a reusable function:

from src.predict import predict_tampering

result = predict_tampering("path/to/image.jpg")

This allows the detection functionality to be integrated with the project's frontend or other applications without duplicating the prediction logic.


---

12. Methodology Summary

The final methodology combines image forensics and machine learning.

ELA provides a representation of compression-level differences, while the trained Keras model uses the processed representation to classify the image.

The resulting system provides an automated indication of whether an image is likely to be REAL or TAMPERED.

The prediction should be interpreted as a model-based result rather than definitive proof of image authenticity.

Where to put it

Your repository will then look roughly like:

text
Image-tampering-detection/
├── README.md
├── METHODOLOGY.md       ← ADD THIS
├── .gitignore
├── src/
├── frontend/
└── ...
