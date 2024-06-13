from sqlalchemy.exc import IntegrityError
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
    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Пользователь с таким именем уже существует.")
    finally:
        session.close()
