from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User
from backend.models.request import Request
from backend.config.gemini_config import DAILY_UPLOAD_LIMIT

def init_app(app):
    student_bp = Blueprint("student", __name__, url_prefix="/api/student")

    # -------------------
    # Submit Request
    # -------------------
    @student_bp.route("/request", methods=["POST"])
    @jwt_required()
    def submit_request():
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404

            data = request.get_json()
            if not data or not data.get("title") or not data.get("description"):
                return jsonify({"message": "Missing title or description"}), 400

            # Daily upload limit
            today = db.func.date(db.func.current_timestamp())
            count_today = Request.query.filter(
                Request.student_id == user_id,
                db.func.date(Request.date_submitted) == today
            ).count()

            if count_today >= DAILY_UPLOAD_LIMIT:
                return jsonify({
                    "message": f"Daily limit of {DAILY_UPLOAD_LIMIT} requests reached"
                }), 403

            # Gemini disabled – safe default
            duplicate_score = 0.0

            new_request = Request(
                student_id=user_id,
                title=data["title"],
                description=data["description"],
                ai_duplicate_score=duplicate_score
            )

            db.session.add(new_request)
            db.session.commit()

            return jsonify({
                "message": "Request submitted successfully",
                "duplicate_score": duplicate_score
            }), 201

        except Exception as e:
            print("submit_request error:", e)
            return jsonify({"message": "Internal server error"}), 500

    # -------------------
    # Get Student Requests
    # -------------------
    @student_bp.route("/requests", methods=["GET"])
    @jwt_required()
    def get_requests():
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404

            requests_list = (
                Request.query
                .filter_by(student_id=user_id)
                .order_by(Request.date_submitted.desc())
                .all()
            )

            return jsonify([req.to_dict() for req in requests_list]), 200

        except Exception as e:
            print("get_requests error:", e)
            return jsonify({"message": "Internal server error"}), 500

    # -------------------
    # Dashboard
    # -------------------
    @student_bp.route("/dashboard", methods=["GET"])
    @jwt_required()
    def dashboard():
        try:
            user_id = int(get_jwt_identity())

            return jsonify({
                "total_requests": Request.query.filter_by(student_id=user_id).count(),
                "pending": Request.query.filter_by(student_id=user_id, status="Pending").count(),
                "approved": Request.query.filter_by(student_id=user_id, status="Approved").count(),
                "rejected": Request.query.filter_by(student_id=user_id, status="Rejected").count()
            }), 200

        except Exception as e:
            print("dashboard error:", e)
            return jsonify({"message": "Internal server error"}), 500

    app.register_blueprint(student_bp)
