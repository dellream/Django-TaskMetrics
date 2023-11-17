from django.urls import path
from .views import TestLoggingView

urlpatterns = [
    # Тестовый путь для проверки логирования
    path('test_logging/', TestLoggingView.as_view(), name='test_logging'),
]
