# Инструкция по развороту инструмента миграций

## Установка python 3.10
```sudo apt-get install python3```

```sudo apt-get install python3-setuptools```

```sudo apt-get install python3-pip```

## Установка mysqlclient
```sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config```

```sudo apt install libffi-dev```

```pip install mysqlclient```

```pip install mysql-connector-python```

## Настройка проекта
Ввести логин и пароль для бд (для windows):
```
set DB_USER=ваше_имя_пользователя
set DB_PASS=ваш_пароль
``` 
Ввести логин и пароль для бд (для linux):
```
export DB_USER=ваше_имя_пользователя
export DB_PASS=ваш_пароль
```

```pip install -r requirements.txt``` // Установка необходимых библиотек

## Команды alembic
```alembic revision --autogenerate -m "<название_миграции>"``` // Создание новой миграции

```alembic upgrade head``` // Применение всех новых миграций к базе данных

```alembic downgrade -1``` // Откат последней миграции

```alembic downgrade <id версии>``` // Откат до указанной миграции

```alembic history``` // Вывод истории миграций

```alembic current``` // Вывод текущей версии базы данных

```alembic heads``` // Вывод идентификаторов вершин миграций (последних миграций)

```alembic branches``` // Вывод всех миграций, которые не были применены

```alembic show <id версии>``` // Отображение кода миграции