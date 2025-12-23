from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.attendance import Attendance
from backend.models.user import User

attendance_bp = Blueprint("attendance_bp", __name__)

@attendance_bp.route("/status", methods=["GET"])
@jwt_required()
def attendance_status():
    try:
        identity = get_jwt_identity()

        # Find user properly (identity may be ERP / roll_no / email)
        user = User.query.filter(
            (User.id == identity) |
            (User.roll_no == identity) |
            (User.email == identity)
        ).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        attendance = Attendance.query.filter_by(student_id=user.id).first()

        # AUTO DUMMY DATA FOR DEMO
        if not attendance:
            attendance = Attendance(
                student_id=user.id,
                total_classes=120,
                attended_classes=96
            )
            db.session.add(attendance)
            db.session.commit()

        percentage = round(
            (attendance.attended_classes / attendance.total_classes) * 100, 2
        ) if attendance.total_classes > 0 else 0

        return jsonify({
            "total_classes": attendance.total_classes,
            "attended_classes": attendance.attended_classes,
            "attendance_percentage": percentage
        }), 200

    except Exception as e:
        print("Attendance status error:", e)
        return jsonify({"error": "Internal server error"}), 500


def init_app(app):
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
