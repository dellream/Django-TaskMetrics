from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Тестовый путь для проверки логирования
    path('test_logging/',
         views.TestLoggingView.as_view(),
         name='test_logging'),

    # Чат-комната
    path('room/<int:course_id>/',
         views.course_chat_room,
         name='course_chat_room'),


]
