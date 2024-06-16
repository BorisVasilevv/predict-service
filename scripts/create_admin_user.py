from models.base import Session
from models.user import User
from models.role import Role
from models.address import Address
from models.specialization import Specialization
from models.user_specialization import user_specialization
from models.pending_user import PendingUser
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


def create_user(username, password, email, first_name, last_name, phone_number, street, house, city, zip_code,
                patronymic=None, flat=None, region=None):
    session = Session()

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Создание записи адреса
    address = Address(
        street=street, house=house, flat=flat,
        city=city, region=region, zip_code=zip_code
    )
    session.add(address)
    session.commit()

    # Создание нового пользователя с указанной ролью и хэшированным паролем
    new_user = User(
        username=username, password=hashed_password, email=email,
        first_name=first_name, last_name=last_name, patronymic=patronymic,
        phone_number=phone_number, address_id=address.id, role_id=1
    )

    try:
        session.add(new_user)
        session.commit()
        print("пользователь создан!")
    except IntegrityError:
        session.rollback()
        print("Error occurred: пользователь с заданным именем или электронной почтой уже существует")
    finally:
        session.close()


# Ввод данных пользователя
username = input("Enter username: ")
password = input("Enter password: ")
email = "None"
first_name = "None"
last_name = "None"
phone_number = "None"
street = "None"
house = "None"
city = "None"
zip_code = "None"

# Пустой список специализаций
specializations = []

# Создание пользователя
create_user(username, password, email, first_name, last_name, phone_number, street, house, city, zip_code, 'admin')
