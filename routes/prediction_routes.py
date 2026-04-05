from flask import Blueprint, request, jsonify
from services.prediction_service import prediction_service
from database.models import PredictionHistory

prediction_bp = Blueprint("prediction_bp", __name__, url_prefix="/api")


@prediction_bp.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No input data provided"
            }), 400

        required_fields = [
            "patient_name",
            "age",
            "gender",
            "pregnancies",
            "glucose",
            "blood_pressure",
            "skin_thickness",
            "insulin",
            "bmi",
            "diabetes_pedigree",
            "age_level"
        ]

        missing_fields = [
            field for field in required_fields
            if field not in data or str(data[field]).strip() == ""
        ]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        result = prediction_service.predict_diabetes(data)

        return jsonify({
            "success": True,
            "message": "Diabetes prediction completed successfully",
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"Invalid input: {str(e)}"
        }), 400

    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500


@prediction_bp.route("/predict/heart", methods=["POST"])
def predict_heart():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No input data provided"}), 400

        required_fields = [
            "patient_name", "age", "gender",
            "chest_pain", "resting_bp", "cholesterol",
            "fasting_bs", "rest_ecg", "max_heart_rate",
            "exercise_angina", "oldpeak", "slope", "ca", "thal"
        ]

        missing_fields = [field for field in required_fields if field not in data or str(data[field]).strip() == ""]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        result = prediction_service.predict_heart(data)

        return jsonify({
            "success": True,
            "message": "Heart disease prediction completed successfully",
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "message": f"Invalid input: {str(e)}"}), 400
    except FileNotFoundError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@prediction_bp.route("/predict/breast-cancer", methods=["POST"])
def predict_breast_cancer():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No input data provided"}), 400

        required_fields = [
            "patient_name", "age", "gender",
            "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
            "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
            "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
            "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
            "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
            "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
        ]

        missing_fields = [field for field in required_fields if field not in data or str(data[field]).strip() == ""]

        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        result = prediction_service.predict_breast_cancer(data)

        return jsonify({
            "success": True,
            "message": "Breast cancer prediction completed successfully",
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "message": f"Invalid input: {str(e)}"}), 400
    except FileNotFoundError as e:
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@prediction_bp.route("/history", methods=["GET"])
def get_history():
    try:
        records = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).all()

        return jsonify({
            "success": True,
            "count": len(records),
            "data": [record.to_dict() for record in records]
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@prediction_bp.route("/history/<int:history_id>", methods=["GET"])
def get_single_history(history_id):
    try:
        record = PredictionHistory.query.get(history_id)

        if not record:
            return jsonify({
                "success": False,
                "message": "Record not found"
            }), 404

        return jsonify({
            "success": True,
            "data": record.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500