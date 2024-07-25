#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

cp -r static/. /backend_static/static/

DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_PASSWORD=admin \
python manage.py createsuperuser --noinput

gunicorn --reload -b 0.0.0.0:8000 -w 2 main.wsgi