# backend/config/gemini_config.py

import os

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent")
# Duplicate detection settings
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))# similarity score threshold to flag duplicates
DAILY_UPLOAD_LIMIT = 3        # max issues a student can report per day
