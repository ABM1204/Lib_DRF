#Lib-API

## Описание

#Это API для управления книгами и авторами. Система 
позволяет пользователям добавлять книги и авторов, просматривать 
список книг, получать подробную информацию о каждой книге, редактировать и 
удалять их. Также реализована функциональность избранных книг для 
пользователей и периодические задачи для работы с данными.



#Инструкция по установке

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ABM1204/Lib_DRF.git
```

2. Установите виртуальное окружение:
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:
- На Windows:
  ```bash
  venv\Scripts\activate
  ```
- На macOS/Linux:
  ```bash
  venv/bin/activate
  ``` 

4. Установите зависимости: 
```bash
pip install -r requirements.txt
```

5. Перейдите в директорию проекта:
```bash
cd source
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя (по желанию):
```bash
python manage.py createsuperuser
```

8. Запустите сервер:
```bash
python manage.py runserver
```


#Маршруты
```bash
admin/              - админка
api/                - API
api/register/       - Регистрация пользователя
api/token/          - Получение access и refresh токенов 
api/token/refresh/  - Получение обновлние токена
api/logout/         - Выход с учётной записи
schema/             - Схема API
docs/               - Документация
```


## Технологии

- python 3.12.1
- Django 5.1.5
- Postgresql
- DRF 3.15.2
- JWT-token
- Swager
- Pytest
- Celery


