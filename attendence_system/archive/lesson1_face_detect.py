import cv2

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

img_path = "data/Selim/001.jpg"
img = cv2.imread(img_path)
if img is None:
    raise RuntimeError(f"Image not found: {img_path}")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

print("Faces detected:", len(faces))

# ❌ Reject if no face
if len(faces) == 0:
    raise RuntimeError("No face detected. Image rejected.")

# ✅ Pick the biggest face (by area)
largest_face = None
max_area = 0

for x, y, w, h in faces:
    area = w * h
    if area > max_area:
        max_area = area
        largest_face = (x, y, w, h)

x, y, w, h = largest_face

# Draw only ONE rectangle (the real face)
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

out_path = "lesson1_output_filtered.jpg"
cv2.imwrite(out_path, img)
print("Saved:", out_path)

cv2.imshow("Filtered Face Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
