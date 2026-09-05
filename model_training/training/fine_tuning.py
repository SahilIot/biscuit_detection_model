import sys # locate the shared config module
from pathlib import Path

from ultralytics import YOLO
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

# PATHS
# EXISTING MODEL THAT YOU WANT TO FINE-TUNE (override MODEL_PATH in your .env)
MODEL_PATH = config.MODEL_PATH
# NEW YOLO DATASET CREATED BY semi_auto_label.py
DATASET = str(config.DATASET_YAML)

# TRAINING SETTINGS
EPOCHS = 40
IMAGE_SIZE = 640
BATCH_SIZE = 4
# CHECK PATHS
print()
print("=" * 70)
print("BISCUIT MODEL FINE-TUNING")
print("=" * 70)
print()
if not os.path.exists(MODEL_PATH):
    print("ERROR: Existing model not found:")
    print(MODEL_PATH)
    raise SystemExit
if not os.path.exists(DATASET):
    print("ERROR: Dataset YAML not found:")
    print(DATASET)
    raise SystemExit
print("Existing model:")
print(MODEL_PATH)
print()
print("Fine-tuning dataset:")
print(DATASET)
print()

# LOAD EXISTING MODEL

print("Loading existing YOLO model...")
model = YOLO(MODEL_PATH)
print("Model loaded successfully.")
print()

# FINE-TUNING
print("=" * 70)
print("STARTING FINE-TUNING")
print("=" * 70)
print()
results = model.train(
    # DATASET
    data=DATASET,
    # TRAINING
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    batch=BATCH_SIZE,
    # CPU
    device="cpu",
    # REPRODUCIBILITY
    seed=42,
    # DATA AUGMENTATION
    degrees=5,
    translate=0.05,
    scale=0.20,
    shear=2,
    perspective=0.0005,
    fliplr=0.5,
    flipud=0.0,
    hsv_h=0.015,
    hsv_s=0.4,
    hsv_v=0.25,
    # MOSAIC
    mosaic=0.5,
    close_mosaic=10,
    # OPTIMIZER

    optimizer="AdamW",
    # LOW LEARNING RATE BECAUSE WE ARE FINE-TUNING
    lr0=0.0005,
    lrf=0.01,
    weight_decay=0.0005,
    warmup_epochs=2,

    # VALIDATION
    val=True,
    plots=True,

    # OUTPUT
    project=str(config.RUNS_DIR),
    name="biscuit_v3",
    exist_ok=True,
    save=True,
    save_period=10,

    # CPU WORKERS
    workers=0,
    verbose=True
)

# FINISHED
print()
print("=" * 70)
print("FINE-TUNING COMPLETE")
print("=" * 70)
print()

print("New model:")
print(config.RUNS_DIR / "biscuit_v3" / "weights" / "best.pt")
print()
print("Use this new best.pt for your next detection test.")
print()