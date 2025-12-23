from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models.user import User
from flask_jwt_extended import create_access_token
import datetime

def init_app(app):
    auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

    # -------------------
    # Register Route (ERP only)
    # -------------------
    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        if not data or not all(k in data for k in ("name", "roll_no", "password")):
            return jsonify({"message": "Missing required fields"}), 400

        # Check if ERP already exists
        if User.query.filter_by(roll_no=data["roll_no"]).first():
            return jsonify({"message": "User with this ERP ID already exists"}), 400

        new_user = User(
            name=data["name"],
            roll_no=data["roll_no"]
        )
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    # -------------------
    # Login Route (ERP only)
    # -------------------
    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data or not all(k in data for k in ("erp", "password")):
            return jsonify({"message": "Missing ERP ID or password"}), 400

        user = User.query.filter_by(roll_no=data["erp"]).first()

        if not user or not user.check_password(data["password"]):
            return jsonify({"message": "Invalid ERP ID or password"}), 401

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=datetime.timedelta(days=1)
        )

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    app.register_blueprint(auth_bp)
