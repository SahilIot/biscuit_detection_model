# Biscuit Detection — Model Training & Counting Pipeline

Computer vision project for detecting, tracking, counting, and measuring biscuits moving on a conveyor belt using YOLO, OpenCV, video input, and Hikvision CCTV.

The project is organized so that source code and configuration can be shared through GitHub while large datasets, videos, model weights, and generated outputs remain local or are stored separately.

---

## 1. Project Goal

The main goal of this project is to build a reliable conveyor-belt vision system that can:

- Detect biscuits on a moving conveyor.
- Track individual biscuits.
- Count biscuits crossing defined lines.
- Measure biscuit size where required.
- Handle camera vibration and small camera movement.
- Work with recorded conveyor videos.
- Work with a Hikvision CCTV camera through RTSP.
- Provide information for future PLC integration.
- Eventually operate as a real-time production system.

The development pipeline is:

```text
Video / Hikvision Camera
        ↓
Frame Extraction
        ↓
Data Preparation
        ↓
Annotation
        ↓
YOLO Training
        ↓
Fine-Tuning
        ↓
Model Evaluation
        ↓
Real-World Video Testing
        ↓
Detection
        ↓
Tracking
        ↓
Counting / Measurement
        ↓
Deployment
        ↓
PLC Integration


```
## 2. Repository Structure
```text


model_training/
|
├──.github
|     └──workflows
|      └──ci.yml
│
├── archive/
│   └── test_biscuit.py
│
├── counting/
│   ├── detailing.py
|   ├── count_biscuits.py
|   ├── count_line.py
│   ├── horizontal.py
│   ├── vertical.py
│   ├── test.py
│   └── size_measure.py
│   
├── data/
│   ├── biscuit_dataset/
│   │   ├── images/
│   │   │   ├── train/
│   │   │   ├── val/
│   │   │   └── test/
│   │   │
│   │   ├── labels/
│   │   │   ├── train/
│   │   │   ├── val/
│   │   │   └── test/
│   │   │
│   │   └── data.yaml
│   │
│   ├── empty_frames/
│   ├── raw_frames/
│   └── videos/
│
├── data_prep/
|     ├── empty_conveyor_data.py
|     ├── generate_data.py
|     ├── semi_auto_label.py
│
├── deployment/
|        ├── cctv_check.py
|        ├── video_detection.py
│
├── evaluation/
|        ├── test_model.py
|        ├── test_model_photos.py
│
├── models/
│   ├── best.pt
│   └── runs/
│       └── detect/
│
├── outputs/
│   └── diagnostic_results/
|── test/
|      └──test_config.py
|      └──test_count_biscuits.py
│
├── training/
│   ├── fine_tuning.py
│   └── train_model.py
│
├── .env
├── .env.example
├── .gitignore
├── config.py
├── README.md
└── requirements.txt
```

## 3 Folder Responsibilities
```
counting/

Contains object tracking, counting, and measurement logic.
Typical functionality includes:

Line-based counting.
Horizontal line counting.
Vertical line counting.
Object tracking.
Object crossing detection.
Biscuit size measurement.
Counting validation.

Several scripts may represent different experiments.

When a final implementation is selected, 
it should become the main production version and older
 alternatives should be moved to archive/.
 
 data/
 Contains local dataseta and input data.
 Large files inside this directory are intentionally not commited to Github.
 
 data/biscuit_dataset/
 Contains the YOLO dataset.
 Structure:
 
 data/biscuit_dataset/
│
├── images/
│   ├── train/
│   ├── val/
│   └── test/
│
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
│
└── data.yaml

The images and labels may become very large, so they should normally be stored outside GitHub.
The data.yaml file should be committed because it is part of the dataset configuration.

data/videos/
Contains local conveyor videos
Videos are not committed to Github.

data/empty_frames/
Contains frames of an empty conveyor.

These can be used for:

Background modeling.
Camera stabilization.
Motion detection.
Background subtraction.
Empty-conveyor reference generation.
These files are not committed to GitHub.

data_prep/

Contains scripts used to prepare the training data.

Examples:

Video frame extraction.
Image filtering.
Dataset organization.
Annotation conversion.
Train/validation/test splitting.
Dataset cleanup.


training/

Contains model training and fine-tuning scripts.

training/
├── trainmodel.py
└── fine_tuning.py

Training scripts should use paths from config.py instead of hardcoded computer-specific paths.


evaluation/

Contains model evaluation scripts.
Evaluation should be performed using both the YOLO validation dataset and real conveyor videos.
Important evaluation metrics include:

Precision.
Recall.
mAP50.
mAP50-95.
False positives.
False negatives.
Detection stability.
Counting accuracy.

models/

Contains local trained model files and training runs.
Recommended structure:

models/
├── best.pt
└── runs/
    └── detect/
        └── experiment_name/

The canonical local model path is:
models/best.pt
Model weights are intentionally excluded from GitHub.

outputs/

Contains generated results.

Examples:
Diagnostic videos.
Detection videos.
Debug images.
Tracking results.
Counting results.
Evaluation output.
Experimental results.

Generated files are normally excluded from GitHub.


deployment/

Contains the final deployment and real-time inference code.
Possible components include:

Hikvision RTSP input.
VLC/OpenCV video input.
YOLO inference.
Camera stabilization.
Object tracking.
Counting.
Conveyor monitoring.
PLC communication

```
## 4 Configuration
```text
 config.py

config.py is the central configuration file for the project.

The purpose is to prevent individual scripts from containing hardcoded computer-specific paths.

Bad:

MODEL_PATH = r"C:\Users\Sahil\Downloads\model_training\models\runs\detect\biscuit_v3\weights\best.pt"

Good:

from config import MODEL_PATH

The same approach should be used for:

VIDEO_PATH
DATASET_DIR
DATASET_YAML
MODELS_DIR
OUTPUTS_DIR

This allows the project to work on different computers without modifying every script.


```
## 5 Environment Variables
```text
Machine-specific settings and sensitive information are stored in .env.

Example .env:

MODEL_PATH=models/best.pt
BASE_MODEL_PATH=yolo26n.pt
VIDEO_PATH=data/videos/v1.mp4

CAMERA_IP=YOUR_CAMERA_IP
CAMERA_USERNAME=admin
CAMERA_PASSWORD=YOUR_PASSWORD

The .env file must never be committed to GitHub.

A template should be committed:

.env.example

Example .env.example:

MODEL_PATH=models/best.pt
BASE_MODEL_PATH=yolo26n.pt
VIDEO_PATH=data/videos/v1.mp4

CAMERA_IP=YOUR_CAMERA_IP
CAMERA_USERNAME=admin
CAMERA_PASSWORD=YOUR_PASSWORD

Each developer creates their own .env from .env.example.
```
## 6 Installation
```text
 Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd model_training
Create a Virtual Environment
Windows
python -m venv .venv

Activate:

.venv\Scripts\activate
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

Activate:

source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
```
## 7 Create .env
```text
Do not copy .env from another developer.

Create your own local .env.

Windows PowerShell
Copy-Item .env.example .env
Linux / macOS
cp .env.example .env

Then edit:

.env

and enter your local configuration
```
## 8 Dataset Preparation
```text
The training dataset should follow the YOLO directory structure:

data/biscuit_dataset/
│
├── images/
│   ├── train/
│   ├── val/
│   └── test/
│
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
│
└── data.yaml

For every image there should normally be a corresponding label file.

Example:

images/train/biscuit_001.jpg
labels/train/biscuit_001.txt
```

## 9 Annotation Guidelines
```text
The dataset should contain realistic conveyor conditions.

Important situations to include:

Single biscuit.
Multiple biscuits.
Biscuits touching each other.
Overlapping biscuits.
Different biscuit orientations.
Different biscuit positions on the conveyor.
Partially visible biscuits.
Motion blur.
Different conveyor speeds.
Different lighting conditions.
Camera vibration.
Shadows.
Difficult background areas.
Empty conveyor.

The goal is not simply to collect many images.

The goal is to collect images that represent the conditions the final system will encounter.
```

## 10 Training
```text
Training scripts are located in:

training/

Main scripts:

training/trainmodel.py
training/fine_tuning.py

Before training, verify:

Dataset path is correct.
data.yaml is correct.
Images are present.
Labels are present.
Class names are correct.
Train/validation/test splits are correct.
GPU is available if GPU training is intended.
```
## 11 Training Experiments
```text
Every important training experiment should be recorded.

Recommended experiment information:

Experiment ID:
Date:
Dataset version:
Base model:
Epochs:
Image size:
Batch size:
Learning rate:
Precision:
Recall:
mAP50:
mAP50-95:
Notes:

Example:

Experiment ID: EXP-001
Dataset version: biscuit-v1
Base model: YOLO
Epochs: 100
Image size: 640
Batch size: 16

Precision: ...
Recall: ...
mAP50: ...
mAP50-95: ...

Notes:
Initial training experiment.

This makes it easier to compare models later
```

## 12 Model Selection
```text
Do not select a model based on only one metric.

Consider:

Precision.
Recall.
mAP50.
mAP50-95.
False positives.
False negatives.
Detection performance on real conveyor videos.
Counting accuracy.
Stability across different videos.

A model with a higher validation score is not automatically the best production model.

Real-world conveyor testing is required.
```

