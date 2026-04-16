import os
import pickle
import cv2
import config
from face_engine import FaceEngine

def build_database():
    if not os.path.isdir(config.DATA_DIR):
        print(f"Error: Data folder not found at {config.DATA_DIR}")
        print("Please create it and add subfolders for each person (e.g. data/Selim/, data/John/)")
        return

    print("Initializing Face Engine...")
    engine = FaceEngine()
    
    total = 0
    skipped = 0

    print(f"Scanning directory: {config.DATA_DIR}")
    # Loop over subdirectories (each represents a person)
    for person_name in sorted(os.listdir(config.DATA_DIR)):
        person_dir = os.path.join(config.DATA_DIR, person_name)
        
        # Skip files, only process directories
        if not os.path.isdir(person_dir):
            continue

        print(f"\nProcessing person: {person_name}")
        person_embeddings = []
        
        for filename in sorted(os.listdir(person_dir)):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            total += 1
            img_path = os.path.join(person_dir, filename)
            img = cv2.imread(img_path)

            if img is None:
                skipped += 1
                print(f"  [SKIP] unreadable: {filename}")
                continue

            faces = engine.detect_faces(img)
            if not faces:
                skipped += 1
                print(f"  [SKIP] no face: {filename}")
                continue
            
            # Use the largest face if multiple are found
            face = engine.get_biggest_face(faces)
            emb = engine.get_embedding(face)

            person_embeddings.append(emb)
            print(f"  [OK] {filename}")
            
        if person_embeddings:
            out_path = os.path.join(person_dir, "embedding.pkl")
            with open(out_path, "wb") as f:
                pickle.dump(person_embeddings, f)
            print(f"  -> Saved {len(person_embeddings)} embeddings to {out_path}")

    print("\n--- Summary ---")
    print(f"Total images processed: {total}")
    print(f"Skipped images: {skipped}")
    print("Database built successfully!")

if __name__ == "__main__":
    build_database()
