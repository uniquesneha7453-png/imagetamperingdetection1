"""
Dataset Validation Module

Inspects the dataset directory and validates the readiness of training data:
  - Counts valid image files in dataset/real and dataset/tampered
  - Supports: .jpg, .jpeg, .png, .bmp, .webp
  - Checks for empty classes
  - Checks for severe class imbalance
  - Safely handles non-existent or empty directories without crashing
"""

import sys
from pathlib import Path

# Supported image file extensions
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def check_dataset(dataset_dir="dataset"):
    """
    Validates and summarizes the training dataset.

    Args:
        dataset_dir (str | Path): Path to the dataset root folder.

    Returns:
        dict: Summary containing counts, readiness status, and warnings.
    """
    dataset_path = Path(dataset_dir).resolve()
    real_dir = dataset_path / "real"
    tampered_dir = dataset_path / "tampered"

    real_images = []
    tampered_images = []

    if real_dir.exists():
        real_images = [
            p for p in real_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS
        ]

    if tampered_dir.exists():
        tampered_images = [
            p for p in tampered_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in VALID_EXTENSIONS
        ]

    real_count = len(real_images)
    tampered_count = len(tampered_images)
    total_count = real_count + tampered_count

    warnings = []
    is_ready = True

    # 1. Directory and empty class checks
    if not dataset_path.exists():
        warnings.append(f"Dataset root directory does not exist: {dataset_path}")
        is_ready = False
    elif not real_dir.exists():
        warnings.append("Subdirectory 'dataset/real/' is missing.")
        is_ready = False
    elif not tampered_dir.exists():
        warnings.append("Subdirectory 'dataset/tampered/' is missing.")
        is_ready = False

    if real_count == 0:
        warnings.append("Class 'real' is empty (0 images).")
        is_ready = False
    if tampered_count == 0:
        warnings.append("Class 'tampered' is empty (0 images).")
        is_ready = False

    # 2. Severe imbalance check
    if real_count > 0 and tampered_count > 0:
        ratio = max(real_count, tampered_count) / min(real_count, tampered_count)
        if ratio >= 3.0:
            dominant = "REAL" if real_count > tampered_count else "TAMPERED"
            warnings.append(
                f"Severe class imbalance detected ({ratio:.1f}:1). "
                f"'{dominant}' has significantly more samples. Consider balancing classes."
            )

    return {
        "dataset_dir": str(dataset_path),
        "real_count": real_count,
        "tampered_count": tampered_count,
        "total_count": total_count,
        "is_ready": is_ready,
        "warnings": warnings,
    }


def print_report(results):
    """
    Formats and prints the dataset validation results to console.
    """
    print("=" * 55)
    print("       DATASET VALIDATION REPORT")
    print("=" * 55)
    print(f"Directory:       {results['dataset_dir']}")
    print(f"REAL count:      {results['real_count']}")
    print(f"TAMPERED count:  {results['tampered_count']}")
    print(f"TOTAL count:     {results['total_count']}")
    print("-" * 55)

    if results["warnings"]:
        print("WARNINGS / NOTICES:")
        for w in results["warnings"]:
            print(f"  [!] {w}")
        print("-" * 55)

    if results["is_ready"]:
        print("STATUS: READY FOR TRAINING")
    else:
        print("STATUS: NOT READY FOR TRAINING")
        print("Images still need to be added to dataset/real and dataset/tampered before training.")
    print("=" * 55)


if __name__ == "__main__":
    dir_arg = sys.argv[1] if len(sys.argv) > 1 else "dataset"
    validation_results = check_dataset(dir_arg)
    print_report(validation_results)
