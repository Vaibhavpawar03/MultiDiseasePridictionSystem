import os
import json
import joblib
import numpy as np
from config import Config
from utils.input_mapper import map_level, map_yes_no, map_gender
from database.models import db, PredictionHistory


class PredictionService:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self._load_models()

    def _load_models(self):
        for disease, path in Config.MODEL_PATHS.items():
            if os.path.exists(path):
                self.models[disease] = joblib.load(path)

        for disease, path in Config.SCALER_PATHS.items():
            if os.path.exists(path):
                self.scalers[disease] = joblib.load(path)

    def _get_risk_level(self, confidence):
        if confidence < 0.40:
            return "Low"
        elif confidence < 0.70:
            return "Medium"
        return "High"

    def _predict_with_model(self, disease, features):
        if disease not in self.models:
            raise FileNotFoundError(f"Model for '{disease}' not found. Train and save it first.")

        model = self.models[disease]
        scaler = self.scalers.get(disease)

        X = np.array(features, dtype=float).reshape(1, -1)

        if scaler is not None:
            X = scaler.transform(X)

        prediction = model.predict(X)[0]

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.85

        return int(prediction), round(confidence, 4)

    def predict_diabetes(self, data):
        patient_name = data.get("patient_name", "").strip()
        age = int(data.get("age", 0))
        gender = data.get("gender", "male")
        sex = map_gender(gender)

        pregnancies = float(data.get("pregnancies", 0))
        glucose = map_level(data.get("glucose"))
        blood_pressure = map_level(data.get("blood_pressure"))
        skin_thickness = map_level(data.get("skin_thickness"))
        insulin = map_level(data.get("insulin"))
        bmi = map_level(data.get("bmi"))
        diabetes_pedigree = map_level(data.get("diabetes_pedigree"))
        age_level = map_level(data.get("age_level"))

        features = [
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age,
            sex,
            age_level
        ]

        prediction, confidence = self._predict_with_model("diabetes", features)

        result_text = "Diabetic" if prediction == 1 else "Not Diabetic"
        risk_level = self._get_risk_level(confidence)

        saved = self._save_history(
            patient_name=patient_name,
            age=age,
            gender=gender,
            disease_type="Diabetes",
            input_data=data,
            prediction_result=result_text,
            confidence=confidence,
            risk_level=risk_level
        )

        return {
            "history_id": saved.id,
            "disease": "Diabetes",
            "prediction": prediction,
            "result": result_text,
            "confidence": confidence,
            "risk_level": risk_level
        }

    def predict_heart(self, data):
        patient_name = data.get("patient_name", "").strip()
        age = int(data.get("age", 0))
        gender = data.get("gender", "male")

        sex = map_gender(gender)
        chest_pain = float(data.get("chest_pain", 0))
        resting_bp = map_level(data.get("resting_bp"))
        cholesterol = map_level(data.get("cholesterol"))
        fasting_bs = map_yes_no(data.get("fasting_bs"))
        rest_ecg = float(data.get("rest_ecg", 0))
        max_heart_rate = map_level(data.get("max_heart_rate"))
        exercise_angina = map_yes_no(data.get("exercise_angina"))
        oldpeak = map_level(data.get("oldpeak"))
        slope = float(data.get("slope", 0))
        ca = float(data.get("ca", 0))
        thal = float(data.get("thal", 0))

        features = [
            age,
            sex,
            chest_pain,
            resting_bp,
            cholesterol,
            fasting_bs,
            rest_ecg,
            max_heart_rate,
            exercise_angina,
            oldpeak,
            slope,
            ca,
            thal
        ]

        prediction, confidence = self._predict_with_model("heart", features)

        result_text = "Heart Disease Detected" if prediction == 1 else "No Heart Disease"
        risk_level = self._get_risk_level(confidence)

        saved = self._save_history(
            patient_name=patient_name,
            age=age,
            gender=gender,
            disease_type="Heart Disease",
            input_data=data,
            prediction_result=result_text,
            confidence=confidence,
            risk_level=risk_level
        )

        return {
            "history_id": saved.id,
            "disease": "Heart Disease",
            "prediction": prediction,
            "result": result_text,
            "confidence": confidence,
            "risk_level": risk_level
        }

    def predict_breast_cancer(self, data):
        patient_name = data.get("patient_name", "").strip()
        age = int(data.get("age", 0))
        gender = data.get("gender", "female")

        radius_mean = map_level(data.get("radius_mean"))
        texture_mean = map_level(data.get("texture_mean"))
        perimeter_mean = map_level(data.get("perimeter_mean"))
        area_mean = map_level(data.get("area_mean"))
        smoothness_mean = map_level(data.get("smoothness_mean"))
        compactness_mean = map_level(data.get("compactness_mean"))
        concavity_mean = map_level(data.get("concavity_mean"))
        concave_points_mean = map_level(data.get("concave_points_mean"))
        symmetry_mean = map_level(data.get("symmetry_mean"))
        fractal_dimension_mean = map_level(data.get("fractal_dimension_mean"))
        radius_se = map_level(data.get("radius_se"))
        texture_se = map_level(data.get("texture_se"))
        perimeter_se = map_level(data.get("perimeter_se"))
        area_se = map_level(data.get("area_se"))
        smoothness_se = map_level(data.get("smoothness_se"))
        compactness_se = map_level(data.get("compactness_se"))
        concavity_se = map_level(data.get("concavity_se"))
        concave_points_se = map_level(data.get("concave_points_se"))
        symmetry_se = map_level(data.get("symmetry_se"))
        fractal_dimension_se = map_level(data.get("fractal_dimension_se"))
        radius_worst = map_level(data.get("radius_worst"))
        texture_worst = map_level(data.get("texture_worst"))
        perimeter_worst = map_level(data.get("perimeter_worst"))
        area_worst = map_level(data.get("area_worst"))
        smoothness_worst = map_level(data.get("smoothness_worst"))
        compactness_worst = map_level(data.get("compactness_worst"))
        concavity_worst = map_level(data.get("concavity_worst"))
        concave_points_worst = map_level(data.get("concave_points_worst"))
        symmetry_worst = map_level(data.get("symmetry_worst"))
        fractal_dimension_worst = map_level(data.get("fractal_dimension_worst"))

        features = [
            radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
            compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean,
            radius_se, texture_se, perimeter_se, area_se, smoothness_se,
            compactness_se, concavity_se, concave_points_se, symmetry_se, fractal_dimension_se,
            radius_worst, texture_worst, perimeter_worst, area_worst, smoothness_worst,
            compactness_worst, concavity_worst, concave_points_worst, symmetry_worst, fractal_dimension_worst
        ]

        prediction, confidence = self._predict_with_model("breast_cancer", features)

        result_text = "Breast Cancer Detected" if prediction == 1 else "No Breast Cancer"
        risk_level = self._get_risk_level(confidence)

        saved = self._save_history(
            patient_name=patient_name,
            age=age,
            gender=gender,
            disease_type="Breast Cancer",
            input_data=data,
            prediction_result=result_text,
            confidence=confidence,
            risk_level=risk_level
        )

        return {
            "history_id": saved.id,
            "disease": "Breast Cancer",
            "prediction": prediction,
            "result": result_text,
            "confidence": confidence,
            "risk_level": risk_level
        }

    def _save_history(self, patient_name, age, gender, disease_type, input_data, prediction_result, confidence, risk_level):
        record = PredictionHistory(
            patient_name=patient_name,
            age=age,
            gender=gender,
            disease_type=disease_type,
            input_data=json.dumps(input_data),
            prediction_result=prediction_result,
            confidence=confidence,
            risk_level=risk_level
        )
        db.session.add(record)
        db.session.commit()
        return record


prediction_service = PredictionService()