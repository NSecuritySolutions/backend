FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN pip install gunicorn==20.1.0


CMD gunicorn --reload -b 0.0.0.0:8000 -w 2 main.wsgi