import re

from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash, generate_password_hash
from models.base import Session
from models.user import User


def authenticate_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def user_has_role(user_id, role_name):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return user.role.name == role_name if user.role else False
        return False
    finally:
        session.close()


def create_user(username: str, password: str):
    hashed_password = generate_password_hash(password)

    # Создайте сессию и добавьте нового пользователя
    session = Session()
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()


def is_password_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
