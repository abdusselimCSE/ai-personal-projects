import numpy as np
from insightface.app import FaceAnalysis
import config

class FaceEngine:
    def __init__(self):
        self.app = FaceAnalysis(name=config.MODEL_NAME)
        # We use ctx_id=0 for CPU/CoreML and standard det_size
        self.app.prepare(ctx_id=0, det_size=config.DET_SIZE)

    def detect_faces(self, frame_bgr):
        """
        Returns a list of face objects detected in the frame.
        """
        return self.app.get(frame_bgr)

    @staticmethod
    def get_biggest_face(faces):
        """
        Given a list of faces, returns the largest one by bounding box area.
        """
        if not faces:
            return None
        return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))

    @staticmethod
    def get_embedding(face):
        """
        Normalizes and returns the 512D embedding for a given face.
        """
        emb = face.embedding.astype(np.float32)
        emb = emb / np.linalg.norm(emb)
        return emb

    @staticmethod
    def cosine_similarity(emb1, emb2):
        """
        Returns the cosine similarity between two normalized embeddings.
        """
        return float(np.dot(emb1, emb2))
