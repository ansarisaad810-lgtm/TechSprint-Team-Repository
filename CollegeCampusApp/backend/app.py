from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Initialize DB and JWT
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # -------------------------------------------------
    # FORCE SINGLE DATABASE (NO DUPLICATES EVER AGAIN)
    # -------------------------------------------------
    os.makedirs(app.instance_path, exist_ok=True)

    DB_PATH = os.path.join(app.instance_path, "collegecampus_v2.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "superjwtsecretkey")

    # Init extensions
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)

    # -------------------------------------------------
    # IMPORT MODELS (IMPORTANT)
    # -------------------------------------------------
    from backend.models.user import User
    from backend.models.request import Request
    from backend.models.attendance import Attendance
    from backend.models.lostfound import LostFound
    from backend.models.issue import Issue

    # -------------------------------------------------
    # CREATE TABLES + SEED DATA
    # -------------------------------------------------
    with app.app_context():
        print("Using database:", DB_PATH)

        db.create_all()

        # -------------------------
        # Seed demo user
        # -------------------------
        try:
            if User.query.count() == 0:
                demo = User(name="Demo Student", roll_no="100001")
                demo.set_password("password")
                db.session.add(demo)
                db.session.commit()
                print("Inserted demo user")
        except Exception as e:
            print("Demo user seeding error:", e)

        # -------------------------
        # Ensure requested user
        # -------------------------
        requested_erp = "6605791"
        try:
            user = User.query.filter_by(roll_no=requested_erp).first()
            if not user:
                user = User(name="Md Saad Ansari", roll_no=requested_erp)
                user.set_password("123456")
                db.session.add(user)
                db.session.commit()
                print("Restored user ERP:", requested_erp)
            else:
                if user.name != "Md Saad Ansari":
                    user.name = "Md Saad Ansari"
                    db.session.commit()
        except Exception as e:
            print("User restore error:", e)

        # -------------------------
        # FORCE DUMMY ATTENDANCE
        # -------------------------
        try:
            user = User.query.filter_by(roll_no=requested_erp).first()
            if user:
                attendance = Attendance.query.filter_by(student_id=user.id).first()
                if not attendance:
                    attendance = Attendance(
                        student_id=user.id,
                        total_classes=120,
                        attended_classes=96
                    )
                    db.session.add(attendance)
                    db.session.commit()
                    print("Inserted dummy attendance for user_id:", user.id)
                else:
                    # Ensure values are correct
                    attendance.total_classes = 120
                    attendance.attended_classes = 96
                    db.session.commit()
        except Exception as e:
            print("Attendance seed error:", e)

    # -------------------------------------------------
    # REGISTER ROUTES
    # -------------------------------------------------
    from backend.routes.auth_routes import init_app as auth_init
    from backend.routes.attendance_routes import init_app as attendance_init
    from backend.routes.helpdesk_routes import init_app as helpdesk_init
    from backend.routes.lostfound_routes import init_app as lostfound_init
    from backend.routes.materials_routes import init_app as materials_init
    from backend.routes.timetable_routes import init_app as timetable_init
    from backend.routes.student_routes import init_app as student_init

    auth_init(app)
    attendance_init(app)
    helpdesk_init(app)
    lostfound_init(app)
    materials_init(app)
    timetable_init(app)
    student_init(app)

    # -------------------------------------------------
    # SERVE FRONTEND
    # -------------------------------------------------
    app.static_folder = "../frontend/www"
    app.static_url_path = ""

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        file_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(file_path):
            return app.send_static_file(path)
        return app.send_static_file("index.html")

    # Serve Uploads
    from flask import send_from_directory
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        uploads_dir = os.path.join(app.instance_path, '../uploads') # Backend/uploads
        # Adjust path if needed based on structure
        # app.py is in backend/, uploads is in backend/uploads
        # app.instance_path is usually backend/instance
        # Let's rely on standard path relative to app.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uploads_dir = os.path.join(base_dir, 'uploads')
        return send_from_directory(uploads_dir, filename)

    return app

