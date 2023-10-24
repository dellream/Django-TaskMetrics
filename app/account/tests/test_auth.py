import time

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config.conf import HOME_URL


@pytest.mark.usefixtures('browser')
class TestBasicUserAuth:
    def test_home_page(self, client: Client) -> None:
        """Вход на домашнюю страницу"""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        print('\ntest_home_page: Получена домашняя страница')

    @pytest.mark.django_db
    def test_register(
            self,
            client: Client,
            browser
    ) -> None:
        """
        Проверка регистрации пользователя
        через форму регистрации
        """
        browser.get(HOME_URL)
        print('\ntest_register: Получена домашняя страница')
        response = client.get(HOME_URL)
        assert response.status_code == 200

        # Регистрация нового пользователя
        register_button = browser.find_element(By.CLASS_NAME, 'register')
        register_button.click()
        response = client.get(reverse('register'))
        assert response.status_code == 200
        print('test_register: Переход на страницу регистрации')

        # Поиск полей для регистрации
        username_input = browser.find_element(By.ID, 'id_username')
        first_name_input = browser.find_element(By.ID, 'id_first_name')
        email_input = browser.find_element(By.ID, 'id_email')
        password_input = browser.find_element(By.ID, 'id_password')
        confirm_password_input = browser.find_element(By.ID, 'id_password2')

        # Внесение данных в поля
        username_input.send_keys('test_register_username')
        first_name_input.send_keys('test_register_first_name')
        email_input.send_keys('test_register_email@test.test')
        password_input.send_keys('test_register_password')
        confirm_password_input.send_keys('test_register_password')
        # time.sleep(3)

        create_acc_button = browser.find_element(By.XPATH, '//input[@value="Создать мой аккаунт"]')
        create_acc_button.click()

        # Проверка, создан ли такой пользователь
        user = User.objects.get(username='test_register_username')
        print(f'test_register: Пользователь "test_register_username" найден в БД')
        assert user.username == 'test_register_username'

        # Тут нужно обратиться к основной БД, а не тестовой и проверить, появился ли пользователь с username
        # test_register_username, в админке он появляется, то есть код правильный, как это в тест загнать?

    print('\ntest_register: Регистрация завершена')


    # @pytest.mark.django_db
    # def test_login(self, client, test_user):
    #     """
    #     Проверка авторизации зарегистрированного
    #     пользователя через форму авторизации
    #     """
    #     client.login(username='testuser', password='testpassword')
    #     response = client.get(reverse('core:home'))
    #     assert response.status_code == 200
    #     # Проверки для авторизованного пользователя
    #
    # @pytest.mark.django_db
    # def test_logout(
    #         self,
    #         client: Client,
    #         browser
    # ) -> None:
    #     """Выход из системы авторизованного пользователя"""
    #     if client.is_authenticated:
    #         browser.get(reverse('core:home'))
    #         print('test_logout: Получена домашняя страница')
    #
    #         home_logout_button = browser.find_element(By.CLASS_NAME, 'logout_logo')
    #         home_logout_button.click()
    #         print('test_logout: Выполнен клик на изображение выхода из системы')
    #
    #         response = client.get(reverse('logged_out'))
    #         assert response.status_code == 200
    #
    # @pytest.mark.django_db
    # def test_delete_user(self, test_user):
    #     user_to_delete = User.objects.get(username='testuser')
    #     user_to_delete.delete()
    #     assert User.objects.filter(username='testuser').count() == 0
    #     # Проверки для удаления пользователя
