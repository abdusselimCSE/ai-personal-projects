import os
import cv2

# --- Settings ---
IMG_PATH = "data/Selim/001.jpg"
OUT_DIR = "cropped_faces"
OUT_NAME = "selim_face_001.jpg"

os.makedirs(OUT_DIR, exist_ok=True)

# Load face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Read image
img = cv2.imread(IMG_PATH)
if img is None:
    raise RuntimeError(f"Image not found: {IMG_PATH}")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
print("Faces detected:", len(faces))

if len(faces) == 0:
    raise RuntimeError("No face detected. Image rejected.")

# Pick biggest face
largest_face = None
max_area = 0
for x, y, w, h in faces:
    area = w * h
    if area > max_area:
        max_area = area
        largest_face = (x, y, w, h)

x, y, w, h = largest_face

# Add a small margin around the face (helps include full face)
margin = 0.20  # 20%
mx = int(w * margin)
my = int(h * margin)

x1 = max(0, x - mx)
y1 = max(0, y - my)
x2 = min(img.shape[1], x + w + mx)
y2 = min(img.shape[0], y + h + my)

# Crop face region
face_crop = img[y1:y2, x1:x2]

# Resize to a standard size (common step for ML pipelines)
face_crop = cv2.resize(face_crop, (224, 224))

# Save cropped face
out_path = os.path.join(OUT_DIR, OUT_NAME)
cv2.imwrite(out_path, face_crop)
print("Saved cropped face:", out_path)

# Show cropped face
cv2.imshow("Cropped Face (224x224)", face_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
