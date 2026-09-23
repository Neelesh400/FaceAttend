import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get('SECRET_KEY', 'faceattend-secure-secret-key-2026-prod-token')
    
    # Database configuration
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
    SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
    
    # Face storage & models
    FACES_DIR = os.path.join(BASE_DIR, 'database', 'faces')
    MODELS_DIR = os.path.join(BASE_DIR, 'face_recognition', 'models')
    HAAR_CASCADE_PATH = os.path.join(MODELS_DIR, 'haarcascade_frontalface_default.xml')
    LBPH_MODEL_PATH = os.path.join(MODELS_DIR, 'face_model.xml')
    LABEL_MAP_PATH = os.path.join(MODELS_DIR, 'labels.json')
    
    # Face Recognition Defaults
    # In LBPH, lower distance = better match. Confidence < 70 is recognized.
    DEFAULT_CONFIDENCE_THRESHOLD = 75.0
    MIN_FACE_SAMPLES_REQUIRED = 5
    MAX_FACE_SAMPLES_REQUIRED = 10
    
    # Attendance Defaults
    DEFAULT_LATE_CUTOFF = '09:30'
    INSTITUTE_NAME = 'FaceAttend Institute of Technology'
    
    # Session config
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
