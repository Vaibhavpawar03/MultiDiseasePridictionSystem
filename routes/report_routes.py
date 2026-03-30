import os
from flask import Blueprint, jsonify, send_file
from services.report_service import report_service

report_bp = Blueprint("report_bp", __name__, url_prefix="/api/report")


@report_bp.route("/generate/<int:history_id>", methods=["GET"])
def generate_report(history_id):
    try:
        report_data = report_service.generate_prediction_report(history_id)

        return jsonify({
            "success": True,
            "message": "PDF report generated successfully",
            "data": {
                "filename": report_data["filename"],
                "download_url": f"/api/report/download/{report_data['filename']}"
            }
        }), 200

    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500


@report_bp.route("/download/<filename>", methods=["GET"])
def download_report(filename):
    try:
        report_path = os.path.join(os.getcwd(), "reports", filename)

        if not os.path.exists(report_path):
            return jsonify({
                "success": False,
                "message": "Report file not found"
            }), 404

        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500