from backend.app import create_app, db
from backend.models.user import User
from backend.models.issue import Issue
from backend.models.attendance import Attendance
from backend.models.lostfound import LostFound
from backend.models.timetable import Timetable

def initialize_database():
    """
    Initialize all database tables.
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
