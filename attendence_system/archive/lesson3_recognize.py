import os
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis

DB_PATH = "embeddings_selim.pkl"
THRESHOLD = 0.40  # adjust later if needed


def build_face_app():
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def get_biggest_face(faces):
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))


def cosine_similarity(a, b):
    return float(np.dot(a, b))


def recognize_from_frame(app, frame_bgr, selim_embeddings):
    faces = app.get(frame_bgr)
    if len(faces) == 0:
        return {"name": "Unknown", "score": 0.0, "reason": "no_face"}

    face = get_biggest_face(faces)
    emb = face.embedding.astype(np.float32)
    emb = emb / np.linalg.norm(emb)

    scores = [cosine_similarity(emb, e) for e in selim_embeddings]
    best_score = max(scores)

    if best_score >= THRESHOLD:
        return {"name": "Selim", "score": round(best_score, 4), "reason": "matched"}
    return {
        "name": "Unknown",
        "score": round(best_score, 4),
        "reason": "below_threshold",
    }


def main():
    if not os.path.exists(DB_PATH):
        raise RuntimeError(
            "embeddings_selim.pkl not found. Run lesson3_build_database.py first."
        )

    with open(DB_PATH, "rb") as f:
        db = pickle.load(f)

    selim_embeddings = db["embeddings"]
    app = build_face_app()

    cap = cv2.VideoCapture(0)  # 0 = default camera
    if not cap.isOpened():
        raise RuntimeError("Could not open camera. Check macOS permissions.")

    print("Camera opened.")
    print("Controls: [SPACE]=capture & recognize, [S]=save photo, [Q]=quit")

    last_result = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        # Show last recognition on screen
        if last_result:
            text = f"{last_result['name']}  score={last_result['score']}"
            cv2.putText(
                frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

        cv2.imshow("Attendance Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        # SPACE => capture and recognize
        if key == 32:
            last_result = recognize_from_frame(app, frame, selim_embeddings)
            print("Result:", last_result)

        # S => save current frame to file
        if key == ord("s"):
            os.makedirs("camera_captures", exist_ok=True)
            out_path = os.path.join("camera_captures", "capture.jpg")
            cv2.imwrite(out_path, frame)
            print("Saved:", out_path)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
