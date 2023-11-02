from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'account'

urlpatterns = [
    # Регистрация пользователя
    path('register/', views.user_register, name='register'),

    # Просмотр профиля
    path('profile/<str:slug>/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),

    # Редактирование профиля
    path('profile/<str:slug>/edit', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
