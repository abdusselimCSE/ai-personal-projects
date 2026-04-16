<div align="center">
  <h1>📸 Automated Attendance System</h1>
  <p><strong>A modern, full-stack facial recognition attendance system featuring a Python AI backend and a stunning Flutter mobile app.</strong></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flutter-Mobile-02569B.svg?logo=flutter&logoColor=white" alt="Flutter" />
    <img src="https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/OpenCV-5C3EE8.svg?logo=opencv&logoColor=white" alt="OpenCV" />
    <img src="https://img.shields.io/badge/InsightFace-AI-FF6F00" alt="InsightFace" />
  </p>
</div>

---

## ✨ Key Features

- 👤 **Facial Recognition Engine**: Real-time face detection and matching using **InsightFace** and **OpenCV**.
- 🚀 **High-Performance API**: RESTful API powered by **FastAPI** for low-latency image processing.
- 📱 **Mobile Client**: A beautifully designed **Flutter** app featuring custom camera controls, glassmorphism UI, and haptic feedback.
- 📊 **Robust Logging**: Automatically logs attendance locally to CSV and optionally syncs seamlessly to Google Sheets.
- 🛡️ **Duplicate Prevention**: Built-in logical cooldowns to prevent double-logging attendance for the same person in short periods.

---

## 🏗️ Project Architecture

This repository is organized as a monorepo containing both the frontend and backend implementations:

- 📂 **`attendance_app/`**: The modern Flutter mobile application.
- 📂 **`attendence_system/`**: The Python FastAPI & computer vision recognition service.

### Backend Overview (`attendence_system/`)
- `api.py` — The core REST endpoint (`/recognize`).
- `database.py` — Engine to parse `data/` and build face embeddings.
- `main.py` — A standalone webcam-based recognition loop for testing.
- `logger.py` — Handles CSV persistence and Google Sheets webhook integration.
- `config.py` — Configuration variables (thresholds, timings, etc.).

---

## 🛠️ Setup & Installation

### 1. Python Backend
First, ensure you have Python 3.10+ installed.

```bash
# Clone the repository
git clone https://github.com/abdusselimCSE/ai-personal-projects.git
cd ai-personal-projects/attendence_system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn opencv-python numpy insightface pillow requests python-multipart python-dotenv
```

### 2. Building the Face Database
Add your training images into folders corresponding to the person's name:
```text
attendence_system/data/<PersonName>/img1.jpg
...
```
Then, compute and cache the facial embeddings:
```bash
python attendence_system/database.py
```

### 3. Flutter Mobile App
Ensure you have the Flutter SDK installed.
```bash
cd attendance_app

# Get packages
flutter pub get

# Run on an attached device or emulator
flutter run
```

---

## 🚀 Usage Guide

### Running the API Server 🌐
This kicks off the FastAPI server so the mobile client can connect and dispatch face images for immediate ID verification:
```bash
cd attendence_system
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
*Note: Make sure your mobile device and computer are on the same network, and enter your computer's IP address into the app's settings.*

### Running Standalone Webcam Mode 💻
If you prefer not to use the mobile app, you can run recognition directly from your computer's webcam:
```bash
cd attendence_system
python main.py
```

---

## ⚙️ Configuration & Environment

Settings like API thresholds and cooldown durations can be adjusted inside `attendence_system/config.py`. 

### Google Sheets Sync
If using Google Sheets logging, simply create a `.env` file in the root of the project to securely house your target macro URL:
```env
GOOGLE_SHEETS_URL=https://script.google.com/macros/s/YOUR_MACRO_ID/exec
```

---
<div align="center">
  <i>Built with ❤️ using Python and Flutter.</i>
</div>
