import os
import pickle
import numpy as np
import cv2
from insightface.app import FaceAnalysis

INPUT_DIR = "data/Selim"
OUT_PATH = "embeddings_selim.pkl"


def build_face_app():
    app = FaceAnalysis(name="buffalo_l")
    # ctx_id=0 is fine; on Mac it will use CPU/CoreML depending on availability
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


def get_biggest_face(faces):
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))


def main():
    if not os.path.isdir(INPUT_DIR):
        raise RuntimeError(f"Folder not found: {INPUT_DIR}")

    app = build_face_app()

    embeddings = []
    total = 0
    skipped = 0

    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        total += 1
        path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(path)

        if img is None:
            skipped += 1
            print("SKIP unreadable:", filename)
            continue

        faces = app.get(img)
        if len(faces) == 0:
            skipped += 1
            print("SKIP no face:", filename)
            continue

        face = get_biggest_face(faces)

        # embedding already represents the aligned face internally
        emb = face.embedding.astype(np.float32)
        emb = emb / np.linalg.norm(emb)

        embeddings.append(emb)
        print("OK:", filename)

    if len(embeddings) == 0:
        raise RuntimeError("No embeddings created. Add clearer face photos.")

    with open(OUT_PATH, "wb") as f:
        pickle.dump({"name": "Selim", "embeddings": embeddings}, f)

    print("\n--- Summary ---")
    print("Total images:", total)
    print("Embeddings saved:", len(embeddings))
    print("Skipped:", skipped)
    print("Saved file:", OUT_PATH)


if __name__ == "__main__":
    main()
