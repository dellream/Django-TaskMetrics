import time

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config.conf import HOME_URL, LOGIN_URL, REGISTER_URL


class TestBasicUserAuth:
    def test_home_page(self, client: Client) -> None:
        """Вход на домашнюю страницу"""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        print('\ntest_home_page: Получена домашняя страница')

    @pytest.mark.django_db
    def test_register(self, driver) -> None:
        """
        Проверка регистрации пользователя
        через форму регистрации
        """
        try:
            # Проверим, есть ли уже тестовый пользователь:
            user = User.objects.get(username='test_register_username')
            assert user.username == 'test_register_username'
            print(f'\ntest_register: Пользователь "test_register_username" уже существует в БД')
            # Если пользователь уже существует, завершаем тест неудачей
            assert False
        except User.DoesNotExist:
            driver.get(HOME_URL)
            assert driver.current_url == HOME_URL
            print('\ntest_register: Получена домашняя страница')

            # Регистрация нового пользователя
            register_button = driver.find_element(By.CLASS_NAME, 'register')
            register_button.click()
            assert driver.current_url == REGISTER_URL
            print('test_register: Переход на страницу регистрации')

            # Поиск полей для регистрации
            username_input = driver.find_element(By.ID, 'id_username')
            first_name_input = driver.find_element(By.ID, 'id_first_name')
            email_input = driver.find_element(By.ID, 'id_email')
            password_input = driver.find_element(By.ID, 'id_password')
            confirm_password_input = driver.find_element(By.ID, 'id_password2')

            # Внесение данных в поля
            username_input.send_keys('test_register_username')
            first_name_input.send_keys('test_register_first_name')
            email_input.send_keys('test_register_email@test.test')
            password_input.send_keys('test_register_password')
            confirm_password_input.send_keys('test_register_password')
            # time.sleep(3)

            create_acc_button = driver.find_element(By.XPATH, '//input[@value="Создать мой аккаунт"]')
            create_acc_button.click()

            # Проверка, создан ли такой пользователь
            user = User.objects.get(username='test_register_username')
            assert user.username == 'test_register_username'
            print(f'test_register: Пользователь "test_register_username" найден в БД')

            # Тут нужно обратиться к основной БД, а не тестовой и проверить, появился ли пользователь с username
            # test_register_username, в админке он появляется, то есть код правильный, как это в тест загнать?

            print('\ntest_register: Регистрация завершена')

    @pytest.mark.django_db
    def test_login(self, driver) -> None:
        """
        Проверка авторизации зарегистрированного
        пользователя через форму авторизации
        """
        driver.get(HOME_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        assert driver.current_url == HOME_URL
        print('\ntest_login: Получена домашняя страница')

        header_login_button = driver.find_element(By.CLASS_NAME, 'login')
        header_login_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        assert driver.current_url == LOGIN_URL
        print('test_login: Переход на страницу авторизации успешно выполнен')

        # Находим поля для ввода
        username_input = driver.find_element(By.ID, 'id_username')
        password_input = driver.find_element(By.ID, 'id_password')

        # Вводим данные с прошлого теста
        username_input.send_keys('test_register_username')
        password_input.send_keys('test_register_password')

        login_button = driver.find_element(By.XPATH, '//input[@value="Войти"]')
        login_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        assert driver.current_url == HOME_URL
        print('test_login: Редирект после авторизации произошел')
