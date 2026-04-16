import os
import pickle
import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File
import config
from face_engine import FaceEngine
from logger import AttendanceLogger
import io
from PIL import Image

app = FastAPI(title="Attendance Recognition API")

# Global instances
engine = None
logger = None
known_embeddings = []
known_names = []

@app.on_event("startup")
def startup_event():
    global engine, logger, known_embeddings, known_names
    print("Starting API: Initializing Face Engine...")
    engine = FaceEngine()
    logger = AttendanceLogger()

    print("Loading distributed databases...")
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

    print(f"Loaded {len(known_embeddings)} embeddings.")

@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    # Read the image file sent from the Flutter app
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Convert PIL Image to OpenCV format (BGR)
    img_np = np.array(image)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    faces = engine.detect_faces(img_bgr)
    
    if not faces:
        return {"status": "error", "message": "No face detected in the image."}
        
    results = []
    
    for face in faces:
        emb = engine.get_embedding(face)
        
        best_score = 0
        best_name = "Unknown"
        
        for known_emb, known_name in zip(known_embeddings, known_names):
            score = engine.cosine_similarity(emb, known_emb)
            if score > best_score:
                best_score = score
                best_match = known_name

        if best_score >= config.MATCH_THRESHOLD:
            best_name = best_match
            
            # Log attendance and pass the status down
            status_code = logger.log_attendance(best_name)

        results.append({
            "name": best_name,
            "score": float(best_score),
            "status": status_code if best_score >= config.MATCH_THRESHOLD else "UNKNOWN",
            "bbox": face.bbox.tolist()
        })
        
    return {"status": "success", "faces": results}
