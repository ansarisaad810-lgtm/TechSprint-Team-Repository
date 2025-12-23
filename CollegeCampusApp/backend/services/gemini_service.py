# backend/services/gemini_service.py

from backend.config.gemini_config import SIMILARITY_THRESHOLD
from difflib import SequenceMatcher

def analyze_image(image_path):
    """
    Gemini disabled (invalid REST usage).
    Return None to force local duplicate logic.
    """
    return None

def is_duplicate(new_description, existing_descriptions):
    if not new_description:
        return False

    for desc in existing_descriptions:
        if not desc:
            continue
        ratio = SequenceMatcher(None, new_description, desc).ratio()
        if ratio >= SIMILARITY_THRESHOLD:
            return True
    return False
