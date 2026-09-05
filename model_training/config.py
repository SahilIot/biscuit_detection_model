"""
config.py
=========

Central, machine-independent configuration for the whole biscuit
detection pipeline (data prep -> labeling -> training -> fine-tuning
-> evaluation -> counting -> live deployment).

WHY THIS FILE EXISTS
---------------------
The original scripts each hardcoded one person's local path, e.g.:

    MODEL_PATH = r"C:\\Users\\Sahil\\Downloads\\WelcomeScreen\\runs\\detect\\..."

That only works on one laptop. The moment a second person clones the
repo, every script breaks (wrong OS, wrong username, wrong folder).

Instead:
    - Shared folders (data/, models/, outputs/) are defined ONCE here,
      relative to the project root, so they work identically for
      everyone regardless of OS or username.
    - Anything that's genuinely personal or secret (which video file
      you're testing with locally, camera IP/credentials) is read
      from a local ".env" file that is NEVER committed to git
      (see .gitignore). Copy .env to .env and fill in your
      own values.

Every script in this repo should import its paths from here instead
of hardcoding them.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ============================================================
# PROJECT ROOT
# ============================================================
# This file lives at the project root, so its own folder IS the root.
PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")


def _env_path(name: str, default_relative: str) -> str:
    """Read a path from the environment, falling back to a path
    relative to the project root so the repo works out of the box
    with no .env at all."""
    value = os.getenv(name)
    return str(Path(value)) if value else str(PROJECT_ROOT / default_relative)


# ============================================================
# SHARED FOLDERS (same for everyone, created automatically)
# ============================================================
DATA_DIR = PROJECT_ROOT / "data"
RAW_VIDEOS_DIR = DATA_DIR / "videos"
RAW_FRAMES_DIR = DATA_DIR / "raw_frames"
EMPTY_FRAMES_DIR = DATA_DIR / "empty_frames"

MODELS_DIR = PROJECT_ROOT / "models"
DATASET_DIR = PROJECT_ROOT / "biscuit_dataset"
DATASET_YAML = DATASET_DIR / "data.yaml"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DIAGNOSTIC_DIR = OUTPUTS_DIR / "diagnostic_results"
RUNS_DIR = PROJECT_ROOT / "runs" / "detect"

for _folder in (RAW_VIDEOS_DIR,RAW_FRAMES_DIR,EMPTY_FRAMES_DIR, MODELS_DIR,DIAGNOSTIC_DIR,):
    _folder.mkdir(parents=True, exist_ok=True)

# MODEL WEIGHTS
# Whatever YOLO weights you personally want scripts to use by
# default. Override per-machine in .env, e.g.:
#   MODEL_PATH=C:\Users\you\runs\detect\biscuit_v3\weights\best.pt
MODEL_PATH = _env_path("MODEL_PATH", "models/best.pt")

# Base/pretrained weights used to START training from scratch
# (see training/train_model.py).
BASE_MODEL_PATH = _env_path("BASE_MODEL_PATH", "yolo26n.pt")

# VIDEO INPUT
# Default local test video. Override in .env per machine, e.g.:
#   VIDEO_PATH=C:\Users\you\Videos\testing_video.mp4
VIDEO_PATH = _env_path("VIDEO_PATH", "data/videos/v1.mp4")


# HIKVISION CAMERA (secrets -- keep these ONLY in your local .env)
CAMERA_IP = os.getenv("CAMERA_IP", "YOUR_IP")
CAMERA_USERNAME = os.getenv("CAMERA_USERNAME", "admin")
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD", "YOUR_PASSWORD")