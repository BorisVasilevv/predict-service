import secrets

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash, generate_password_hash

from models.base import Session
from models.pending_user import PendingUser
from models.role import Role
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


def assign_role_to_user(user_id: int, role_name: str):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        role = session.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise ValueError("Role not found")

        user.role = role
        session.commit()
    finally:
        session.close()


def remove_role_from_user(user_id: int):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        user.role = None
        session.commit()
    finally:
        session.close()


def get_all_users():
    session = Session()
    try:
        users = session.query(User).options(joinedload(User.role)).all()
        return users
    finally:
        session.close()


def get_all_roles():
    session = Session()
    try:
        roles = session.query(Role).all()
        return roles
    finally:
        session.close()
