from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    disease_type = db.Column(db.String(50), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    prediction_result = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "gender": self.gender,
            "disease_type": self.disease_type,
            "input_data": self.input_data,
            "prediction_result": self.prediction_result,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }