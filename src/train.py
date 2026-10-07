"""
Model Training Module

Trains the image tampering detection CNN using Error Level Analysis (ELA) preprocessing.

Expected Dataset Structure:
    dataset/
      real/        <- Authentic, unedited images (Label 0)
      tampered/    <- Manipulated, forged images (Label 1)

Features:
  - Safe dataset verification (gracefully informs user if dataset is not yet present)
  - Train / validation split
  - Batch generation with on-the-fly ELA extraction and normalization
  - Early stopping and model checkpointing
  - Saves the final trained model to outputs/tampering_model.keras
"""

import math
import random
import sys
from pathlib import Path
import numpy as np
import keras

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model import build_tampering_model
from src.preprocessing import prepare_image_for_model

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


class ELADataSequence(keras.utils.PyDataset):
    """
    Keras PyDataset generator that loads and applies ELA preprocessing
    batch-by-batch to conserve RAM.
    """

    def __init__(self, samples, batch_size=16, shuffle=True, **kwargs):
        super().__init__(**kwargs)
        self.samples = list(samples)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indices = np.arange(len(self.samples))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        return max(1, int(math.ceil(len(self.samples) / self.batch_size)))

    def __getitem__(self, idx):
        start = idx * self.batch_size
        end = start + self.batch_size
        batch_indices = self.indices[start:end]

        images, labels = [], []
        for i in batch_indices:
            img_path, label = self.samples[i]
            try:
                # ELA extraction -> resize 224x224 -> RGB -> normalized float32
                img_tensor, _ = prepare_image_for_model(img_path, add_batch_dim=False)
                images.append(img_tensor)
                labels.append(label)
            except Exception as err:
                print(f"[Warning] Failed to process {img_path}: {err}. Skipping.")

        if not images:
            # Fallback zero-array in the rare case all images in a batch failed
            return np.zeros((1, 224, 224, 3), dtype=np.float32), np.zeros((1,), dtype=np.float32)

        return np.array(images, dtype=np.float32), np.array(labels, dtype=np.float32)

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)


def collect_dataset_samples(dataset_dir="dataset"):
    """
    Scans the dataset directory for real and tampered images.

    Returns:
        list[tuple[Path, int]]: List of (image_path, label) pairs.
            0 = REAL
            1 = TAMPERED
    """
    dataset_path = Path(dataset_dir)
    real_dir = dataset_path / "real"
    tampered_dir = dataset_path / "tampered"

    if not dataset_path.exists() or not real_dir.exists() or not tampered_dir.exists():
        return None

    samples = []

    # Collect authentic images (label 0)
    for p in real_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS:
            samples.append((p, 0))

    # Collect tampered images (label 1)
    for p in tampered_dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS:
            samples.append((p, 1))

    return samples


def train_model(
    dataset_dir="dataset",
    output_path="outputs/tampering_model.keras",
    epochs=15,
    batch_size=16,
    val_split=0.2,
    learning_rate=1e-3,
):
    """
    Main training routine.
    """
    print("=" * 60)
    print("  IMAGE TAMPERING DETECTION - MODEL TRAINING")
    print("=" * 60)

    # 1. Check for dataset existence
    samples = collect_dataset_samples(dataset_dir)
    if not samples:
        print("\n[DATASET NOT FOUND OR EMPTY]")
        print(f"Directory checked: {Path(dataset_dir).resolve()}")
        print("\nExpected directory structure:")
        print("  dataset/")
        print("    real/        <- Add authentic images here (Class 0)")
        print("    tampered/    <- Add manipulated images here (Class 1)")
        print("\nTo train later:")
        print("  1. Place your images in 'dataset/real/' and 'dataset/tampered/'")
        print("  2. Run: python src/train.py\n")
        return False

    real_count = sum(1 for _, lbl in samples if lbl == 0)
    tampered_count = sum(1 for _, lbl in samples if lbl == 1)

    print(f"\nFound {len(samples)} total images:")
    print(f"  - Real images (Class 0):     {real_count}")
    print(f"  - Tampered images (Class 1): {tampered_count}")

    if real_count == 0 or tampered_count == 0:
        print("[Error] Both 'real' and 'tampered' folders must contain at least one valid image.")
        return False

    # 2. Shuffle and split into train/validation sets
    random.seed(42)
    random.shuffle(samples)

    split_idx = int(len(samples) * (1.0 - val_split))
    train_samples = samples[:split_idx]
    val_samples = samples[split_idx:]

    print(f"\nDataset Split:")
    print(f"  - Training samples:   {len(train_samples)}")
    print(f"  - Validation samples: {len(val_samples)}")

    train_dataset = ELADataSequence(train_samples, batch_size=batch_size, shuffle=True)
    val_dataset = ELADataSequence(val_samples, batch_size=batch_size, shuffle=False)

    # 3. Build model
    print("\nBuilding model architecture...")
    model = build_tampering_model(learning_rate=learning_rate)

    # 4. Prepare output directory & callbacks
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=str(out_file),
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
    ]

    # 5. Train the model
    print(f"\nStarting training for up to {epochs} epochs (Batch size: {batch_size})...")
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )

    # 6. Save final model
    model.save(str(out_file))
    print(f"\n[Success] Model successfully saved to: {out_file.resolve()}")

    # 7. Print final metrics summary
    print("\n" + "=" * 60)
    print("  TRAINING SUMMARY METRICS")
    print("=" * 60)
    final_epoch = len(history.history["loss"])
    print(f"Completed Epochs: {final_epoch}")
    print(f"Train Loss:      {history.history['loss'][-1]:.4f}")
    print(f"Train Accuracy:  {history.history['accuracy'][-1]:.4%}")
    if "val_loss" in history.history:
        print(f"Val Loss:        {history.history['val_loss'][-1]:.4f}")
        print(f"Val Accuracy:    {history.history['val_accuracy'][-1]:.4%}")
        if "val_precision" in history.history:
            print(f"Val Precision:   {history.history['val_precision'][-1]:.4%}")
        if "val_recall" in history.history:
            print(f"Val Recall:      {history.history['val_recall'][-1]:.4%}")
    print("=" * 60)

    return True


if __name__ == "__main__":
    train_model()
