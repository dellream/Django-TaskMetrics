"""
ASGI-конфигурация для проекта config.

Он предоставляет ASGI-вызываемый объект как переменную модуля с именем ``application``.

Дополнительную информацию по этому файлу можно найти по адресу
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# Устанавливаем значение переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Получаем ASGI-приложение Django
django_asgi_app = get_asgi_application()

# Определяем ASGI-приложение для протокола, используя ProtocolTypeRouter
application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,  # Для обработки HTTP-запросов используем стандартное ASGI-приложение Django
        'websocket': AuthMiddlewareStack(  # Для веб-сокетов применяем стек мидлваров для аутентификации
            URLRouter(chat.routing.websocket_urlpatterns)  # Определяем URL-маршруты для веб-сокетов из chat.routing
        )
    }
)
