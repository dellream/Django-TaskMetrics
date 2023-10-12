from . import views

from django.urls import path

app_name = 'core'

urlpatterns = [
    # Домашняя страница
    path('', views.home_page, name='home'),
]
