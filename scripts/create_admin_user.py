from models.user import User
from models.role import Role
from models.base import Session
from werkzeug.security import generate_password_hash


session = Session()


def create_user(username, password, role_name):
    # Проверяем, существует ли роль с заданным именем
    role = session.query(Role).filter_by(name=role_name).first()
    if not role:
        print(f"Role '{role_name}' does not exist. Please create it first.")
        return

    # Проверяем, существует ли пользователь с заданным именем
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("User with that username already exists.")
        return

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Создаем нового пользователя с указанной ролью и хэшированным паролем
    new_user = User(username=username, password=hashed_password, role=role)
    session.add(new_user)
    session.commit()
    print("User created successfully.")


username = input("Enter username: ")
password = input("Enter password: ")
role_name = "admin"
create_user(username, password, role_name)
