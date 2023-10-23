import pytest
from django.contrib.auth.models import User
from django.test import Client
from selenium import webdriver


@pytest.fixture(scope='class')
def browser():
    """
    Фикстура для получения экземпляра драйвера для Хрома
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def client():
    return Client()
