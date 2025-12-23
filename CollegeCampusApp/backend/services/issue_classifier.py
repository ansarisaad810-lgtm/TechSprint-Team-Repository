# backend/services/issue_classifier.py

def classify_issue(description: str):
    """
    Simple issue classifier based on keywords.
    Returns category string.
    """
    description_lower = description.lower()
    if any(word in description_lower for word in ["drain", "sewer", "pipe"]):
        return "Plumbing"
    elif any(word in description_lower for word in ["bench", "chair", "furniture"]):
        return "Furniture"
    elif any(word in description_lower for word in ["wall", "tile", "paint"]):
        return "Infrastructure"
    elif any(word in description_lower for word in ["window", "glass"]):
        return "Glass/Window"
    elif any(word in description_lower for word in ["water", "leak"]):
        return "Water Leakage"
    else:
        return "Other"
