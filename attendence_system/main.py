import os
import cv2
import pickle
import numpy as np
import config
from face_engine import FaceEngine
from logger import AttendanceLogger

def main():
    # Load embeddings and names from distributed files
    print("Loading databases from data folders...")
    known_embeddings = []
    known_names = []
    
    if os.path.exists(config.DATA_DIR):
        for person_name in sorted(os.listdir(config.DATA_DIR)):
            person_dir = os.path.join(config.DATA_DIR, person_name)
            emb_path = os.path.join(person_dir, "embedding.pkl")
            
            if os.path.isdir(person_dir) and os.path.exists(emb_path):
                with open(emb_path, "rb") as f:
                    person_embs = pickle.load(f)
                    for emb in person_embs:
                        known_embeddings.append(emb)
                        known_names.append(person_name)

    if not known_embeddings:
        print("No embeddings found. Please run database.py to add faces.")
        return

    print("Initializing Engine and Logger...")
    engine = FaceEngine()
    logger = AttendanceLogger()

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("\nCamera started!")
    print("Controls:")
    print("  [Q] - Quit")
    print("Attendance will be logged automatically.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera.")
            break

        # Detect all faces in the frame
        faces = engine.detect_faces(frame)

        for face in faces:
            # Get face bounding box and draw it
            x1, y1, x2, y2 = face.bbox.astype(int)
            emb = engine.get_embedding(face)

            # Compare against known embeddings
            best_score = 0
            best_name = "Unknown"
            
            for known_emb, known_name in zip(known_embeddings, known_names):
                score = engine.cosine_similarity(emb, known_emb)
                if score > best_score:
                    best_score = score
                    best_match = known_name

            if best_score >= config.MATCH_THRESHOLD:
                best_name = best_match

            # Draw bounding box (Green for known, Red for unknown)
            color = (0, 255, 0) if best_name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Display Name and Score
            label = f"{best_name} ({best_score:.2f})"
            cv2.putText(frame, label, (x1, max(y1 - 10, 0)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Attempt to log attendance
            if best_name != "Unknown":
                logger.log_attendance(best_name)

        # Show the frame
        cv2.imshow("Attendance System", frame)

        # Handle keypresses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
