# backend/utils/file_utils.py

import os
from werkzeug.utils import secure_filename

UPLOAD_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

def save_file(file_storage, folder_name):
    """
    Saves uploaded file to specified folder and returns relative path.
    """
    folder_path = os.path.join(UPLOAD_BASE, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    file_path = os.path.join(folder_path, filename)
    file_storage.save(file_path)
    
    # Return web-accessible relative path
    return f"/uploads/{folder_name}/{filename}"

def delete_file(relative_path):
    """
    Deletes file from the filesystem given its relative path.
    """
    if not relative_path:
        return
    
    try:
        # relative_path is usually like "/uploads/issues/filename.ext"
        # We need the absolute path on the server
        
        # 1. Get the project root (where backend/ is)
        # __file__ is backend/utils/file_utils.py
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 2. Clean the relative path
        clean_rel_path = relative_path.lstrip('/').replace('\\', '/')
        
        # 3. Join them
        abs_path = os.path.abspath(os.path.join(backend_dir, clean_rel_path))
        
        # 4. Safety check: ensure the path is within the uploads directory
        # This prevents accidental deletion of system files
        uploads_dir = os.path.abspath(UPLOAD_BASE)
        if not abs_path.startswith(uploads_dir):
            print(f"Safety warning: Attempted to delete file outside uploads dir: {abs_path}")
            return

        if os.path.exists(abs_path) and os.path.isfile(abs_path):
            os.remove(abs_path)
            print(f"Successfully deleted file: {abs_path}")
        else:
            print(f"File not found for deletion: {abs_path}")
            
    except Exception as e:
        print(f"Error in delete_file for {relative_path}: {e}")
