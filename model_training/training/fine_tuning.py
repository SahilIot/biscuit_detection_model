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
    seed=42, # Randomness control
    # DATA AUGMENTATION
    degrees=5, # Rotation of image +-5
    translate=0.05, # image content to move approx. 5% horizontal/vertical
    scale=0.20, # allows approx 20% scaling variation ( smaller,lager -> biscuit can appear)
    shear=2, # slightly distorts the image geometrically
    perspective=0.0005, # help if camera perspective changes slightly
    fliplr=0.5, # 50% probability of flipping left<-> right
    flipud=0.0, # no vertical flipping
    #HSV augmentation
    hsv_h=0.015, # small color shift
    hsv_s=0.4, # can make colors more or less saturated
    hsv_v=0.25, # changes brightness
    # MOSAIC
    mosaic=0.5, # combines multiple training images into one
    close_mosaic=10,

    # OPTIMIZER
    optimizer="AdamW", #optimization algorithm
    # LOW LEARNING RATE BECAUSE WE ARE FINE-TUNING
    lr0=0.0005, #  this changes how aggressively the model changes its weights
    lrf=0.01, # Controls the final learning rate relative to the initial learning rate
    weight_decay=0.0005, # help reduce overfitting don`t let model become unnecessarily complicated
    warmup_epochs=2, # for first 2 epochs , training starts more gently
    # Epoch 1-> gentle start
    # Epoch 2-> warmup
    # Epoch 3 -> normal training

    # VALIDATION
    val=True, # evaluates the model on your validation dataset during training
    plots=True, # generates training graphs,/results

    # OUTPUT
    project=str(config.RUNS_DIR),
    name="biscuit_v3",
    exist_ok=True,
    save=True,
    save_period=10, # save every 10 epochs

    # CPU WORKERS
    workers=0,
    verbose=True # prints detailed training information - about epochs - losses, metrics etc
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