# Attendance Recognition System

Python-based face recognition attendance system with:

- Live face detection and recognition (InsightFace + OpenCV)
- FastAPI endpoint for image-based recognition
- Attendance logging to CSV
- Optional Google Sheets sync for duplicate-safe daily attendance

## Project Structure

This repository is currently focused on:

- `attendence_system/` - backend attendance recognition service

Main files:

- `attendence_system/api.py` - FastAPI API (`/recognize`)
- `attendence_system/database.py` - build face embeddings from `data/`
- `attendence_system/main.py` - webcam-based recognition loop
- `attendence_system/logger.py` - CSV + Google Sheets attendance logging
- `attendence_system/config.py` - thresholds and runtime settings

## Requirements

- Python 3.10+
- Camera access (for webcam mode)
- Dependencies:
  - `fastapi`
  - `uvicorn`
  - `opencv-python`
  - `numpy`
  - `insightface`
  - `pillow`
  - `requests`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install fastapi uvicorn opencv-python numpy insightface pillow requests python-multipart
```

3. Add training images inside:

```text
attendence_system/data/<PersonName>/*.jpg
```

4. Build embeddings:

```bash
python attendence_system/database.py
```

## Run

Run webcam mode:

```bash
python attendence_system/main.py
```

Run API mode:

```bash
uvicorn attendence_system.api:app --reload
```

## Notes

- Attendance is logged in `attendence_system/attendance.csv`.
- Matching threshold and cooldown can be changed in `attendence_system/config.py`.
- The Flutter app folder (`attendance_app/`) is intentionally excluded from this repo push.
