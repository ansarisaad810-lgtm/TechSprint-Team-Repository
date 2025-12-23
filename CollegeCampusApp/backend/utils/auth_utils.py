# backend/utils/auth_utils.py

from backend.models.user import User
from backend.app import db

def create_user(name: str, roll_no: str, password: str, role: str = "student") -> User:
    """Create and persist a User using the project's User model conventions."""
    from backend.config.settings import ROLES
    if role not in ROLES.values():
        role = ROLES['student']

    user = User(name=name, roll_no=roll_no)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(roll_no: str, password: str):
    """Authenticate a user using roll_no (ERP) and the User.check_password helper."""
    user = User.query.filter_by(roll_no=roll_no).first()
    if user and user.check_password(password):
        return user
    return None
