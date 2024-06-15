import secrets

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.security import check_password_hash, generate_password_hash

from models.address import Address
from models.base import Session
from models.pending_user import PendingUser
from models.role import Role
from models.specialization import Specialization
from models.user import User


def delete_user_by_id(user_id: int):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            address = session.query(Address).filter(Address.id == user.address_id).first()
            if address:
                session.delete(address)  # Удаление адреса пользователя
            session.delete(user)  # Удаление самого пользователя
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_by_id(user_id):
    session = Session()
    try:
        user = session.query(User).options(joinedload(User.address), joinedload(User.specializations)).get(user_id)
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_user(user_id, data):
    session = Session()
    try:
        user = session.query(User).options(joinedload(User.address)).get(user_id)
        if not user:
            return {'error': 'User not found'}

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.patronymic = data.get('patronymic')
        user.phone_number = data['phone_number']
        user.email = data['email']

        # Обновление специализаций
        specializations = data['specializations']
        specialization_objects = session.query(Specialization).filter(Specialization.id.in_(specializations)).all()
        user.specializations = specialization_objects

        # Обновление адреса
        address_data = data['address']
        address = user.address
        address.street = address_data['street']
        address.house = address_data['house']
        address.flat = address_data['flat']
        address.city = address_data['city']
        address.region = address_data['region']
        address.zip_code = address_data['zip_code']

        session.commit()
        return {'message': 'User updated successfully'}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


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


def create_user(
    username: str, password: str, email: str, first_name: str, last_name: str,
    patronymic: str, phone_number: str, street: str, house: str, flat: str,
    city: str, region: str, zip_code: str, specializations: list
):
    hashed_password = generate_password_hash(password)
    session = Session()

    # Создание записи адреса
    address = Address(
        street=street, house=house, flat=flat,
        city=city, region=region, zip_code=zip_code
    )
    session.add(address)
    session.commit()

    # Создание нового пользователя
    new_user = User(
        username=username, password=hashed_password, email=email,
        first_name=first_name, last_name=last_name, patronymic=patronymic,
        phone_number=phone_number, address_id=address.id
    )

    # Добавление специализаций
    if specializations:
        for spec_id in specializations:
            specialization = session.query(Specialization).get(spec_id)
            new_user.specializations.append(specialization)

    try:
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Пользователь с таким именем или электронной почтой уже существует.")
    finally:
        session.close()


def create_pending_user(
    username: str, password: str, email: str, first_name: str, last_name: str,
    patronymic: str, phone_number: str, street: str, house: str, flat: str,
    city: str, region: str, zip_code: str, specializations: list
):
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

    new_pending_user = PendingUser(
        username=username, password=hashed_password, email=email, token=token,
        first_name=first_name, last_name=last_name, patronymic=patronymic,
        phone_number=phone_number, street=street, house=house, flat=flat,
        city=city, region=region, zip_code=zip_code
    )

    try:
        session.add(new_pending_user)
        session.commit()
    except IntegrityError as e:
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


def create_address(session, street, house, flat, city, region, zip_code):
    new_address = Address(
        street=street,
        house=house,
        flat=flat,
        city=city,
        region=region,
        zip_code=zip_code
    )
    session.add(new_address)
    session.commit()
    return new_address.id


def create_user_from_pending(session, pending_user, address_id):
    new_user = User(
        username=pending_user.username,
        password=pending_user.password,
        email=pending_user.email,
        first_name=pending_user.first_name,
        last_name=pending_user.last_name,
        patronymic=pending_user.patronymic,
        phone_number=pending_user.phone_number,
        address_id=address_id
    )
    new_user.specializations.extend(pending_user.specializations)
    session.add(new_user)
    session.delete(pending_user)
    session.commit()


def get_user_by_email(email: str):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    finally:
        session.close()


def update_user_password(email: str, new_password: str):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            user.confirmation_code = None  # Удаляем код подтверждения после использования
            session.commit()
    finally:
        session.close()


def save_confirmation_code(email: str, confirmation_code: str):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            user.confirmation_code = confirmation_code
            session.commit()
    finally:
        session.close()
