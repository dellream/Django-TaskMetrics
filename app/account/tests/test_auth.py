import time

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures('browser')
class TestBasicUserAuth:
    def test_home_page(self, client: Client) -> None:
        """Вход на домашнюю страницу"""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200

    def test_register(
            self,
            client: Client,
            browser
    ) -> None:
        """
        Проверка регистрации пользователя
        через форму регистрации
        """
        browser.get(reverse('core:home'))
        time.sleep(10)
        response = client.get(reverse('register'))
        assert response.status_code == 200
        # Регистрация нового пользователя

    @pytest.mark.django_db
    def test_login(self, client, test_user):
        """
        Проверка авторизации зарегистрированного
        пользователя через форму авторизации
        """
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        # Проверки для авторизованного пользователя

    @pytest.mark.django_db
    def test_logout(
            self,
            client: Client,
            browser
    ) -> None:
        """Выход из системы авторизованного пользователя"""
        if client.is_authenticated:
            browser.get(reverse('core:home'))
            print('test_logout: Получена домашняя страница')

            home_logout_button = browser.find_element(By.CLASS_NAME, 'logout_logo')
            home_logout_button.click()
            print('test_logout: Выполнен клик на изображение выхода из системы')

            response = client.get(reverse('logged_out'))
            assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_user(self, test_user):
        user_to_delete = User.objects.get(username='testuser')
        user_to_delete.delete()
        assert User.objects.filter(username='testuser').count() == 0
        # Проверки для удаления пользователя
