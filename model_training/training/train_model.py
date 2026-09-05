import sys # locate the shared config module
from pathlib import Path

from ultralytics import YOLO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config

model = YOLO(config.BASE_MODEL_PATH)
model.train(
    data=str(config.DATASET_YAML),
    epochs=100,
    imgsz=640,
    batch=8,
    patience=20,
    project=str(config.RUNS_DIR),
    name="biscuit_detector"
)