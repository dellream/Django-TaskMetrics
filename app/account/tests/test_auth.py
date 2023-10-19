import pytest
from django.contrib.auth.models import User
from django.urls import reverse


class TestBasicUserAuth:
    def test_home_page(self, client):
        """Проверка домашней страницы"""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_logout(self, client, test_user):
        """Проверка выхода из системы"""
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('logged_out'))
        assert response.status_code == 200

    def test_register(self, client):
        """
        Проверка регистрации пользователя
        через форму регистрации
        """
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
    def test_logout_after_login(self, client, test_user):
        """
        Проверка выхода из системы через интерфейс
        после авторизации
        """
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('logged_out'))
        assert response.status_code == 200
        # Проверки для выхода после авторизации

    @pytest.mark.django_db
    def test_delete_user(self, test_user):
        user_to_delete = User.objects.get(username='testuser')
        user_to_delete.delete()
        assert User.objects.filter(username='testuser').count() == 0
        # Проверки для удаления пользователя
