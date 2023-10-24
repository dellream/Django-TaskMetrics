import pytest
from django.contrib.auth.models import User
from django.test import modify_settings
from django.test import Client
from selenium import webdriver

from app.config import settings
from app.config.conf import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


@pytest.fixture(scope='class')
def browser():
    """
    Фикстура для получения экземпляра драйвера для Хрома
    """
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService(
        executable_path='/home/alexey/prog/Django-TaskMetrics/app/config/chromeDriver/chromedriver'
    )
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options, service=service)
    yield driver
    driver.quit()


@pytest.fixture
def client():
    return Client()


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Фисктура для обращения к основной базе данных
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
