# backend/models/issue.py

from backend.app import db
from datetime import datetime

class Issue(db.Model):
    __tablename__ = "helpdesk_issues"

    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    media_path = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    is_sensitive = db.Column(db.Boolean, default=False)  # hides uploader from students
    status = db.Column(db.String(20), default="Reported")  # Reported / In Progress / Resolved
    duplicate_flag = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploader = db.relationship("User", backref="uploaded_issues")

    def __repr__(self):
        return f"<Issue {self.category} by {self.uploader_id} Status: {self.status}>"
