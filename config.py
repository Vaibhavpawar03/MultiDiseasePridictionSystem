import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "major-project-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "health_app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATHS = {
        "diabetes": os.path.join(BASE_DIR, "models", "diabetes_model.pkl"),
        "heart": os.path.join(BASE_DIR, "models", "heart_model.pkl"),
        "breast_cancer": os.path.join(BASE_DIR, "models", "breast_cancer_model.pkl")
    }

    SCALER_PATHS = {
        "diabetes": os.path.join(BASE_DIR, "models", "diabetes_scaler.pkl"),
        "heart": os.path.join(BASE_DIR, "models", "heart_scaler.pkl"),
        "breast_cancer": os.path.join(BASE_DIR, "models", "breast_cancer_scaler.pkl")
    }