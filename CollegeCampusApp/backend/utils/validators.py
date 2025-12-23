# backend/utils/validators.py

import re

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_erp(erp: str) -> bool:
    # Example ERP validation: numeric and 6-10 digits
    return erp.isdigit() and 6 <= len(erp) <= 10

def is_non_empty_string(value: str) -> bool:
    return isinstance(value, str) and value.strip() != ""
