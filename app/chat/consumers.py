import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Websocket-потребитель для обработки подключений чата.
    """

    async def connect(self):
        """
        Вызывается, когда веб-сокет устанавливает соединение в процессе рукопожатия.

        Извлекает идентификатор курса из URL-параметра, создает уникальное имя группы чат-комнаты,
        присоединяется к группе, принимает соединение и записывает информацию о подключении в лог.
        """
        try:
            # Извлекаем информацию о пользователе
            self.user = self.scope['user']

            # Извлекаем идентификатор курса из URL-параметра
            self.id = self.scope['url_route']['kwargs']['course_id']

            # Создаем уникальное имя группы чат-комнаты
            self.room_group_name = f'chat_{self.id}'

            # Присоединение к группе чат-комнаты
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Принимаем соединение
            await self.accept()
            logger.info(f'WebSocket подключен для пользователя {self.user.username}')
        except Exception as e:
            logger.error(f'Ошибка при подключении WebSocket: {str(e)}')
            await self.close()  # Закрываем соединение при ошибке во время настройки подключения

    async def disconnect(self, close_code):
        """
        Вызывается, когда веб-сокет закрывается по любой причине.

        Покидает группу чат-комнаты и записывает информацию об отключении в лог.
        """
        try:
            # Покинуть группу чат-комнаты
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f'WebSocket отключен для пользователя {self.user.username} с кодом закрытия: {close_code}')
        except Exception as e:
            logger.error(f'Ошибка при отключении WebSocket: {str(e)}')

    async def receive(self, text_data=None, bytes_data=None):
        """
        Вызывается при получении сообщения от веб-сокета.
        Разбирает полученные JSON-данные, извлекает сообщение и отправляет его обратно в веб-сокет.
        """
        try:
            # Разбор полученных JSON-данных
            text_data_json = json.loads(text_data)

            # Парсинг сообщения из JSON-данных
            message = text_data_json['message']

            # Инициализируем текущее время
            now = timezone.now()

            # Отправка сообщения в группу чат-комнаты
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'datetime': now.isoformat(),
                }
            )

            logger.info(f'Сообщение получено и отправлено: {message} от пользователя {self.user.username}')
        except json.JSONDecodeError as e:
            logger.error(f'Ошибка декодирования JSON: {str(e)}')
        except KeyError as e:
            logger.error(f'KeyError при парсинге сообщения: {str(e)}')

    async def chat_message(self, event):
        """
        Получает сообщение из группы чат-комнаты и отправляет его текущему веб-сокету.

        :param event: Событие, содержащее данные о сообщении.
        """
        # Отправляем полученное сообщение текущему веб-сокету
        await self.send(text_data=json.dumps(event))

        logger.info(
            f'Сообщение из группы чат-комнаты отправлено веб-сокету: {event} от пользователя {self.user.username}')
