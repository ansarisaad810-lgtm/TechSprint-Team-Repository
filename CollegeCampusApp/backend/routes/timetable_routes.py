# backend/routes/timetable_routes.py

from flask import Blueprint, request, jsonify
from backend.models.timetable import Timetable

timetable_bp = Blueprint('timetable_bp', __name__)

@timetable_bp.route('/section/<string:section>', methods=['GET'])
def get_timetable(section):
    """
    Returns the timetable for a specific section.
    """
    timetable_entries = Timetable.query.filter_by(section=section).order_by(Timetable.day, Timetable.period_number).all()
    result = []
    for entry in timetable_entries:
        result.append({
            "day": entry.day,
            "period_number": entry.period_number,
            "subject": entry.subject,
            "teacher_name": entry.teacher_name
        })
    return jsonify(result)


def init_app(app):
    """Register the timetable blueprint"""
    app.register_blueprint(timetable_bp, url_prefix='/timetable')
