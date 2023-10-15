from django.urls import path, include
from . import views

urlpatterns = [
    # Встроенные представления аутентификации
    path('', include('django.contrib.auth.urls')),

    # Работа с пользователями
    # Регистрация пользователя
    path('register/', views.user_register, name='user_register'),
    # Редактирование пользователя
    path('edit/', views.user_edit, name='user_edit'),
]
