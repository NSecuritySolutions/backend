# Backend сайта по продаже видеооборудование


## Технологии:
Python 3.11, Django, DRF, Postgres, Docker

### Запустить проект локально
1. Скопировать проект
```python
git clone https://github.com/Maruf995/video.store
```

2. Сделать миграции:
```
docker-compose web run python manage.py makemigrations
docker-compose web run python manage.py migrate
```
3. Создать суперпользователя:
```
docker-compose web run python manage.py createsuperuser
```
4. Запустить проект:
```
docker-compose up
```

Бэкенд будет доступен по адресу `http://localhost`, `http://127.0.0.1`
Админка будет доступена по адресу `http://localhost/admin`

