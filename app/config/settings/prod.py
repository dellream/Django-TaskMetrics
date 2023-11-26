import os

from .base import *

DEBUG = False

ADMINS = [
    ('Aleksey Yakimov', 'yakimov.as@mail.ru'),
]

ALLOWED_HOSTS = ['*']

SECRET_KEY = "django-insecure-o*&rq5s)=ye=i)5s%!5lc-gee@!vu5rc_vf6(zj^ms&#c5un8t"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# # Безопасность
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
