"""
Model Definition Module

Defines a lightweight transfer-learning Convolutional Neural Network (CNN)
architecture for image tampering detection using TensorFlow / Keras.

Pipeline Details:
  - Input Shape: (224, 224, 3)
  - Backbone: MobileNetV2 (efficient, lightweight, fast on CPU)
  - Output: Binary classification with Sigmoid activation
      0 = REAL
      1 = TAMPERED
  - Offline-safe: Does not require downloading pretrained weights if offline.
"""

import keras
from keras import layers


def build_tampering_model(input_shape=(224, 224, 3), pretrained=False, learning_rate=1e-3):
    """
    Builds and compiles a lightweight CNN binary classifier for tampering detection.

    Args:
        input_shape (tuple): Shape of the input tensor (height, width, channels).
                             Defaults to (224, 224, 3).
        pretrained (bool): If True, attempts to load ImageNet weights. If offline or
                           download fails, safely falls back to uninitialized weights.
                           Defaults to False for fast, reliable offline execution.
        learning_rate (float): Learning rate for the Adam optimizer (default: 0.001).

    Returns:
        keras.Model: Compiled Keras model ready for training or inference.
    """
    base_weights = None

    if pretrained:
        try:
            print("Attempting to load MobileNetV2 with ImageNet pretrained weights...")
            base_model = keras.applications.MobileNetV2(
                input_shape=input_shape,
                include_top=False,
                weights="imagenet"
            )
            base_weights = "imagenet"
            print("Successfully loaded ImageNet weights.")
        except Exception as exc:
            print(f"[Notice] Could not load ImageNet weights ({exc}).")
            print("Proceeding with randomly initialized MobileNetV2 (offline mode).")
            base_model = keras.applications.MobileNetV2(
                input_shape=input_shape,
                include_top=False,
                weights=None
            )
    else:
        # Default: lightweight architecture initialized without network dependency
        base_model = keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights=None
        )

    # If pretrained weights were loaded, freeze base layers to prevent overwriting
    if base_weights == "imagenet":
        base_model.trainable = False
    else:
        base_model.trainable = True

    # Build classification head on top of MobileNetV2 features
    inputs = keras.Input(shape=input_shape, name="ela_input")
    x = base_model(inputs)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization(name="batch_norm")(x)
    x = layers.Dropout(0.3, name="dropout_1")(x)
    x = layers.Dense(64, activation="relu", name="dense_features")(x)
    x = layers.Dropout(0.2, name="dropout_2")(x)

    # Single sigmoid output for binary classification:
    # 0 = REAL, 1 = TAMPERED
    outputs = layers.Dense(1, activation="sigmoid", name="tampered_output")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="tampering_detector")

    # Compile with binary cross-entropy and classification metrics
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall")
        ]
    )

    return model


if __name__ == "__main__":
    print("Building model architecture test...")
    test_model = build_tampering_model()
    test_model.summary()
    print("\nModel successfully created and compiled!")
