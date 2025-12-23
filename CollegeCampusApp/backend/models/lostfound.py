# backend/models/lostfound.py

from backend.app import db
from datetime import datetime

class LostFound(db.Model):
    __tablename__ = "lost_found_items"

    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    media_path = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    claimed_by_name = db.Column(db.String(100), nullable=True)
    claimed_by_erp = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default="Available")  # Available / Claimed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploader = db.relationship("User", backref="lostfound_items")

    def __repr__(self):
        return f"<LostFound {self.item_name} Status: {self.status}>"
