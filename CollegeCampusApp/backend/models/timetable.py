# backend/models/timetable.py

from backend.app import db
from datetime import datetime

class Timetable(db.Model):
    __tablename__ = "timetable"

    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # e.g., Monday
    period_number = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    teacher_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Timetable Section {self.section} {self.day} Period {self.period_number}: {self.subject}>"
