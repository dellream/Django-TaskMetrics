from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Определим URL-маршруты для WebSocket с использованием регулярного выражения
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$',  # Ожидает course_id только в виде числа
            consumers.ChatConsumer.as_asgi()),
]
