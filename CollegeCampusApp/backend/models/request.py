from backend.app import db
from datetime import datetime

class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending / Approved / Rejected
    ai_duplicate_score = db.Column(db.Float, default=0.0)  # similarity score from Gemini
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "ai_duplicate_score": self.ai_duplicate_score,
            "date_submitted": self.date_submitted.isoformat()
        }
