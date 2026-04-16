import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_PATH = os.path.join(BASE_DIR, "attendance.csv")

# Face Recognition Settings
MODEL_NAME = "buffalo_l"
DET_SIZE = (640, 640)
MATCH_THRESHOLD = 0.40  # Minimum cosine similarity for a match

# Camera settings
CAMERA_INDEX = 0

# Attendance settings
# Cooldown seconds before a person can be logged again
COOLDOWN_SECONDS = 0 


# Google Sheets Web App URL
GOOGLE_SHEETS_URL = "YOUR_GOOGLE_SHEETS_URL_HERE"
