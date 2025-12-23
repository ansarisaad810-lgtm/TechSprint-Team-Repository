# backend/config/settings.py

import os

# Database configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'db.sqlite3')}"

# App settings
SECRET_KEY = "college_campus_secret_key"  # Replace with a secure key in production

# Roles
ROLES = {
    "student": "student",
    "faculty": "faculty",
    "admin": "admin"
}

# Attendance threshold
ATTENDANCE_CRITERIA = 75  # percentage
