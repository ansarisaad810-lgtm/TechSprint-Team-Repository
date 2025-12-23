# backend/routes/helpdesk_routes.py

from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models.issue import Issue
from backend.models.user import User
from backend.services.gemini_service import analyze_image, is_duplicate
from backend.services.issue_classifier import classify_issue
from backend.utils.file_utils import save_file, delete_file
from datetime import datetime

helpdesk_bp = Blueprint('helpdesk_bp', __name__)

@helpdesk_bp.route('/report', methods=['POST'])
def report_issue():
    """
    Handles new issue reports (image/video) from students.
    """
    try:
        uploader_id = request.form.get('uploader_id')
        category = request.form.get('category')
        description = request.form.get('description', '')
        location = request.form.get('location', '')
        is_sensitive = request.form.get('is_sensitive', 'false').lower() == 'true'
        media_file = request.files.get('media')

        if not all([uploader_id, category, location, media_file]):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate User exists (Fix for 500 error on fresh DB)
        user = User.query.get(uploader_id)
        if not user:
            return jsonify({"error": "Invalid User Session. Please Logout and Login again."}), 400

        # Save file
        media_path = save_file(media_file, "issues")

        # Classify if category is 'Other'
        if category.lower() == 'other':
            try:
                category = classify_issue(description)
            except:
                category = "Other" # Fallback

        # Duplicate detection using Gemini
        try:
            description_embedding = analyze_image(media_path)
            existing_descriptions = [issue.description for issue in Issue.query.all()]
            duplicate_flag = is_duplicate(description_embedding, existing_descriptions) if description_embedding else False
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            duplicate_flag = False

        # Create issue record
        issue = Issue(
            uploader_id=uploader_id,
            category=category,
            description=description,
            location=location,
            media_path=media_path,
            is_sensitive=is_sensitive,
            duplicate_flag=duplicate_flag,
            status="Reported",
            created_at=datetime.utcnow()
        )
        db.session.add(issue)
        db.session.commit()

        return jsonify({
            "message": "Issue reported successfully",
            "issue_id": issue.id,
            "duplicate": duplicate_flag
        }), 201
    except Exception as e:
        print(f"Error reporting issue: {e}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

@helpdesk_bp.route('/list', methods=['GET'])
def list_issues():
    """
    Returns all issues, filtering sensitive issues for students.
    """
    role = request.args.get('role', 'student')
    issues_query = Issue.query.all()
    issues_list = []

    for issue in issues_query:
        data = {
            "id": issue.id,
            "category": issue.category,
            "description": issue.description,
            "location": issue.location,
            "media_path": issue.media_path,
            "status": issue.status,
            "created_at": issue.created_at.isoformat() if issue.created_at else None
        }
        if issue.is_sensitive and role == 'student':
            data["uploader_id"] = None
        else:
            data["uploader_id"] = issue.uploader_id
        issues_list.append(data)

    return jsonify(issues_list)


@helpdesk_bp.route('/remove/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    """
    Deletes an issue by ID.
    """
    try:
        issue = Issue.query.get(issue_id)
        if not issue:
            return jsonify({"error": "Issue not found"}), 404

        # Delete physical file
        delete_file(issue.media_path)

        db.session.delete(issue)
        db.session.commit()

        return jsonify({"message": "Issue deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting issue: {e}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500


def init_app(app):
    """Register the helpdesk blueprint"""
    app.register_blueprint(helpdesk_bp, url_prefix='/helpdesk')
