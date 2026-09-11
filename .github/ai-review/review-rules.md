#AI Code Review Rules

## General

- Review only meaningful problems.
- Do not complain about personal style preferences
- Do not report trivial formatting issues
- Do not suggest unnecessary rewrites.
- Focus on bugs, incorrect behavior, security,performance, maintainability and testing

## Python

- Prefer clear and maintainable Python.
- Use functions with clear responsibilities
- Avoid unnecessary global state
- Handle exceptions appropriately
- Do not silently ignore errors
- Avoid hardcoded configuration values when configuration
 should come from config.py or environment variables.
 

## Project Sturcture
 The main application code is under:
 model_training/
 Tests are under:
 model_training/tests/
 Training-related code is under:
 model_training/training/
 Counting-related code is under:
 model_training/counting/
 Do not suggest unnecessary restructuring

## Configuration
Configuration is handled through:

config.py

Environment-specific secrets should remain in:

.env

Never hardcode secrets, API keys, passwords or credentials.

## Testing

When a PR changes important logic, check whether appropriate
tests exist.

Do not require a separate test file for every Python file.

Focus on behavior and important edge cases.

## Machine Learning

For YOLO/model-training changes, pay attention to:

- Dataset paths
- Dataset configuration
- Model paths
- Image size
- Confidence thresholds
- Device selection
- Training configuration
- Class IDs
- Bounding boxes
- Data leakage
- Train/validation separation
- Incorrect assumptions about model outputs

For counting and detection code, pay attention to:

- Duplicate detections
- Incorrect bounding boxes
- Tracking/counting logic
- Coordinate systems
- Image dimensions
- Frame processing
- Confidence thresholds
- False positives
- False negatives


## Final Decision

AI is only an automated reviewer.

The TL or repository owner makes the final decision
on whether the pull request should be merged.