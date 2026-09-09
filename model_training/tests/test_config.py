from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))

import config

def test_project_root_exists():
    """PROJECT_ROOT should exist and be a directory."""
    assert config.PROJECT_ROOT.exists()
    assert config.PROJECT_ROOT.is_dir()

def test_project_root_is_config_location():
    """config.py should be located directly inside PROJECT_ROOT."""
    config_file = Path(config.__file__).resolve()

    assert config_file.parent == config.PROJECT_ROOT

def test_shared_directories_exist():
    """Required project directories should be created automatically."""
    directories = [
        config.DATA_DIR,
        config.RAW_VIDEOS_DIR,
        config.RAW_FRAMES_DIR,
        config.EMPTY_FRAMES_DIR,
        config.MODELS_DIR,
        config.DIAGNOSTIC_DIR,
    ]

    for directory in directories:
        assert directory.exists()
        assert directory.is_dir()

def test_dataset_paths():
    """Dataset paths should point inside the project."""
    assert config.DATASET_DIR == config.PROJECT_ROOT / "biscuit_dataset"
    assert config.DATASET_YAML == config.DATASET_DIR / "data.yaml"

def test_output_paths():
    """Output paths should have the expected structure."""
    assert config.OUTPUTS_DIR == config.PROJECT_ROOT / "outputs"
    assert config.DIAGNOSTIC_DIR == config.OUTPUTS_DIR / "diagnostic_results"
    assert config.RUNS_DIR == config.PROJECT_ROOT / "runs" / "detect"

def test_model_paths():
    """Default model paths should point to the expected locations."""
    assert config.MODEL_PATH == str(config.PROJECT_ROOT / "models" / "best.pt")
    assert config.BASE_MODEL_PATH == str(config.PROJECT_ROOT / "yolo26n.pt")

def test_video_path():
    """Default video path should point inside data/videos."""
    assert config.VIDEO_PATH == str(config.PROJECT_ROOT / "data" / "videos" / "v1.mp4")

def test_camera_configuration_exists():
    """Camera configuration variables should exist."""
    assert hasattr(config, "CAMERA_IP")
    assert hasattr(config, "CAMERA_USERNAME")
    assert hasattr(config, "CAMERA_PASSWORD")