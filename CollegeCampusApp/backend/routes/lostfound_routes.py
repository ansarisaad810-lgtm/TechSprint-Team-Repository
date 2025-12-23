# backend/routes/lostfound_routes.py

from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models.user import User
from backend.models.lostfound import LostFound
from backend.utils.file_utils import save_file, delete_file
from datetime import datetime

lostfound_bp = Blueprint('lostfound_bp', __name__)

@lostfound_bp.route('/report', methods=['POST'])
def report_item():
    """
    Upload a found item in campus.
    """
    try:
        uploader_id = request.form.get('uploader_id')
        item_name = request.form.get('item_name')
        description = request.form.get('description', '')
        location = request.form.get('location', '')
        media_file = request.files.get('media')

        if not all([uploader_id, item_name, media_file]):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate User exists (Fix for 500 error on fresh DB)
        user = User.query.get(uploader_id)
        if not user:
            return jsonify({"error": "Invalid User Session. Please Logout and Login again."}), 400

        media_path = save_file(media_file, "lostfound")

        item = LostFound(
            uploader_id=uploader_id,
            item_name=item_name,
            description=description,
            location=location,
            media_path=media_path,
            status="Available",
            created_at=datetime.utcnow()
        )
        db.session.add(item)
        db.session.commit()

        return jsonify({"message": "Item reported successfully", "item_id": item.id}), 201
    except Exception as e:
        print(f"Error checking lost item: {e}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

@lostfound_bp.route('/claim', methods=['POST'])
def claim_item():
    """
    Student claims a lost item.
    """
    try:
        data = request.json
        item_id = data.get('item_id')
        claimer_name = data.get('name')
        claimer_erp = data.get('erp')

        if not all([item_id, claimer_name, claimer_erp]):
            return jsonify({"error": "Missing required fields"}), 400

        item = LostFound.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        item.claimed_by_name = claimer_name
        item.claimed_by_erp = claimer_erp
        item.status = "Claimed"

        db.session.commit()

        return jsonify({"message": f"Item {item.item_name} claimed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@lostfound_bp.route('/list', methods=['GET'])
def list_items():
    """
    Returns all lost and found items.
    """
    items = LostFound.query.all()
    items_list = []
    for item in items:
        # Handle potential missing column attribute if DB not migrated
        loc = getattr(item, 'location', 'Unknown')
        items_list.append({
            "id": item.id,
            "item_name": item.item_name,
            "description": item.description,
            "location": loc,
            "media_path": item.media_path,
            "status": item.status,
            "claimed_by_name": item.claimed_by_name,
            "claimed_by_erp": item.claimed_by_erp,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })
    return jsonify(items_list)


@lostfound_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Deletes a lost & found item by ID.
    """
    try:
        item = LostFound.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        # Delete physical file
        delete_file(item.media_path)

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting item: {e}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500


def init_app(app):
    """Register the lost-and-found blueprint"""
    app.register_blueprint(lostfound_bp, url_prefix='/lostfound')
