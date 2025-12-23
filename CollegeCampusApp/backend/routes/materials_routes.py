# backend/routes/materials_routes.py

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

materials_bp = Blueprint('materials_bp', __name__)

MATERIALS_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "materials")
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@materials_bp.route('/list', methods=['GET'])
def list_materials():
    """
    Lists all study materials from the materials folder.
    Returns flat list with metadata stored in JSON files.
    """
    materials_list = []

    if not os.path.exists(MATERIALS_BASE):
        os.makedirs(MATERIALS_BASE, exist_ok=True)
        return jsonify(materials_list)

    # List all files in materials folder
    for filename in os.listdir(MATERIALS_BASE):
        if filename.endswith('.json'):
            # This is metadata file, skip it
            continue
        
        file_path = os.path.join(MATERIALS_BASE, filename)
        if os.path.isfile(file_path):
            # Look for corresponding metadata file
            metadata_file = os.path.join(MATERIALS_BASE, f"{filename}.meta.json")
            metadata = {
                "title": filename,
                "course": "",
                "description": "",
                "type": "Other",
                "uploaded_at": ""
            }
            
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            materials_list.append({
                "filename": filename,
                "title": metadata.get("title", filename),
                "course": metadata.get("course", ""),
                "description": metadata.get("description", ""),
                "type": metadata.get("type", "Other"),
                "uploaded_at": metadata.get("uploaded_at", ""),
                "size": os.path.getsize(file_path)
            })
    
    return jsonify(materials_list)

@materials_bp.route('/upload', methods=['POST'])
def upload_material():
    """
    Upload a study material file with metadata.
    """
    if 'fileUpload' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['fileUpload']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    # Get metadata from form
    title = request.form.get('title', '')
    course = request.form.get('course', '')
    description = request.form.get('description', '')
    material_type = request.form.get('type', 'Other')
    
    # Create materials folder if it doesn't exist
    os.makedirs(MATERIALS_BASE, exist_ok=True)
    
    # Save file with secure filename
    filename = secure_filename(file.filename)
    file_path = os.path.join(MATERIALS_BASE, filename)
    
    # If file already exists, add timestamp to make it unique
    if os.path.exists(file_path):
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{name}_{timestamp}{ext}"
        file_path = os.path.join(MATERIALS_BASE, filename)
    
    file.save(file_path)
    
    # Save metadata
    metadata = {
        "title": title,
        "course": course,
        "description": description,
        "type": material_type,
        "uploaded_at": datetime.now().isoformat()
    }
    
    metadata_file = os.path.join(MATERIALS_BASE, f"{filename}.meta.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    return jsonify({
        "success": True,
        "message": "Material uploaded successfully",
        "filename": filename
    })

@materials_bp.route('/download/<filename>', methods=['GET'])
def download_material(filename):
    """
    Download a material file.
    """
    file_path = os.path.join(MATERIALS_BASE, secure_filename(filename))
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_file(file_path, as_attachment=True)


def init_app(app):
    """Register the materials blueprint"""
    app.register_blueprint(materials_bp, url_prefix='/materials')
