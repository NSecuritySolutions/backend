FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x /code/backend_entrypoint.sh
RUN pip install gunicorn==20.1.0

RUN python manage.py collectstatic --noinput
RUN cp -r static/. /backend_static

CMD gunicorn -b 0.0.0.0:8000 -w 2 main.wsgi
