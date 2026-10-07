# Image Tampering Detection: Real vs Edited

### Detecting Image Manipulation Using Error Level Analysis and Machine Learning

> **PIXELS → EVIDENCE → VERDICT**

## 📌 Overview

Image tampering involves modifying an image using techniques such as
copy-paste, splicing, or retouching.

This project aims to develop a system that detects whether an input image is
likely to be **Real** or **Tampered**.

The system uses **Error Level Analysis (ELA)** to identify regions that may
show inconsistent compression patterns and Machine Learning for classification.

---

## 🎯 Problem Statement

Manipulated images can reduce trust in digital content and create challenges
in areas such as:

- Digital evidence
- Cybersecurity
- Misinformation detection
- Online media verification

The goal of this project is to develop an image-forensics system that can
assist in identifying potentially manipulated images.

---

## 💡 Proposed Solution

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
