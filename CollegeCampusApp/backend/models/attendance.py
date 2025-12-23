from backend.app import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_classes = db.Column(db.Integer, default=0)
    attended_classes = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship("User", backref="attendance_records")

    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.attended_classes / self.total_classes) * 100, 2)

    def classes_needed_for_criteria(self, criteria=75):
        required = ((criteria / 100) * self.total_classes) - self.attended_classes
        return max(0, int(required + 0.999))
