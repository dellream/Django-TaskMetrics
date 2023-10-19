import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def client():
    return Client()
