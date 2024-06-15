import json
from quart import Quart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config.environment
from models.doctor import Specialization


# Настройте движок SQLAlchemy для подключения к вашей базе данных MySQL
engine = create_engine(config.environment.db_url)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    with open('Specialization.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Создайте сессию
    session = Session()

    # Пройдитесь по данным и создайте объекты вашей модели
    for item in data:
        record = Specialization(**item)  # Распакуйте данные в вашу модель
        session.add(record)

    # Сохраните изменения в базе данных
    session.commit()

    print('Records added successfully')
