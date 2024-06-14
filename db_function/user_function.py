import secrets

from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from models.base import Session
from models.pending_user import PendingUser
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


def create_user(username: str, password: str, email: str):
    hashed_password = generate_password_hash(password)
    session = Session()
    new_user = User(username=username, password=hashed_password, email=email)
    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Пользователь с таким именем или электронной почтой уже существует.")
    finally:
        session.close()


def create_pending_user(username: str, password: str, email: str):
    session = Session()

    # Проверка на наличие пользователя с таким именем или почтой
    existing_user = session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        session.close()
        raise ValueError("Пользователь с таким именем или электронной почтой уже существует.")

    hashed_password = generate_password_hash(password)
    token = secrets.token_urlsafe(16)  # Создаем уникальный токен

    new_pending_user = PendingUser(username=username, password=hashed_password, email=email, token=token)

    try:
        session.add(new_pending_user)
        session.commit()
    except IntegrityError as e:
        print(e)
        session.rollback()
        raise ValueError("Ошибка при создании пользователя.")
    finally:
        session.close()

    return token
