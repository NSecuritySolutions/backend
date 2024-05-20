import os
from dotenv import load_dotenv

from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "83(vot%*rpken0wm#0lt!defrrf0%%=hl$ey8(b20%l8a07#f^")  # default key is just for django test

DOMAIN = os.getenv("DOMAIN", "localhost:8000")

# TODO .env
DEBUG = True

# TODO .env
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "*",
    "https://opticontrol.ru/",
    "opticontrol.ru",
]

INSTALLED_APPS = [
    "jazzmin",
    "polymorphic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "product",
    "application",
    "calculator",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.insert(6, "corsheaders")
    MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")

    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN}", f"http://{DOMAIN}"]

ROOT_URLCONF = "main.urls"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('POSTGRES_DB', "djago_db"),
        "USER": os.getenv('POSTGRES_USER', "djago_user"),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD', "django_pass"),
        "HOST": os.getenv('POSTGRES_HOST', "localhost"),
        "PORT": os.getenv('POSTGRES_PORT', 5432),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DATE_INPUT_FORMATS = [
    "%m.%d.%y",
    "%m:%d:%y %H:%M",  # Ни разу не видел чтобы так писали
    "%m.%d.%y %H.%M",  # Ни разу не видел чтобы так писали
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
    "%m/%d/%y %H.%M",  # Ни разу не видел чтобы так писали
    "%m/%d/%y",  # '10/25/06'
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = f'https://{DOMAIN}/'
STATIC_URL = 'static/'

STATIC_ROOT = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SPECTACULAR_SETTINGS = {
    "TITLE": "NSecuritySolutions Project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVERS": [{"url": f"https://{DOMAIN}"}, {"url": f"http://{DOMAIN}"}],
    "COMPONENT_SPLIT_REQUEST": True,
}
