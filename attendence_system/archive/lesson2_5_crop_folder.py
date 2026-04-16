import os
import cv2

INPUT_DIR = "data/Selim"
OUTPUT_DIR = "cropped_faces/Selim"
os.makedirs(OUTPUT_DIR, exist_ok=True)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def crop_biggest_face(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None, "no_face"

    # biggest face
    x, y, w, h = max(faces, key=lambda r: r[2] * r[3])

    # margin
    margin = 0.20
    mx, my = int(w * margin), int(h * margin)

    x1 = max(0, x - mx)
    y1 = max(0, y - my)
    x2 = min(img_bgr.shape[1], x + w + mx)
    y2 = min(img_bgr.shape[0], y + h + my)

    face = img_bgr[y1:y2, x1:x2]
    face = cv2.resize(face, (224, 224))
    return face, "ok"


def main():
    total = 0
    saved = 0
    skipped = 0

    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        total += 1
        path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(path)

        if img is None:
            skipped += 1
            print("SKIP (unreadable):", filename)
            continue

        face, status = crop_biggest_face(img)
        if status != "ok":
            skipped += 1
            print("SKIP (no face):", filename)
            continue

        out_path = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(out_path, face)
        saved += 1
        print("SAVED:", out_path)

    print("\n--- Summary ---")
    print("Total images:", total)
    print("Saved faces:", saved)
    print("Skipped:", skipped)


if __name__ == "__main__":
    main()
