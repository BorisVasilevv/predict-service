from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.environment import db_url

Base = declarative_base()

# Подключение к базе данных
engine = create_engine(db_url)

# Создание сессии
Session = sessionmaker(bind=engine)
