import json
import logging

from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):
    """
    Websocket-потребитель для обработки подключений чата.
    """

    def connect(self):
        """
        Вызывается, когда веб-сокет устанавливает соединение в процессе рукопожатия.
        """
        self.accept()
        logger.info('WebSocket подключен')

    def disconnect(self, close_code):
        """
        Вызывается, когда веб-сокет закрывается по любой причине.
        """
        logger.info('WebSocket отключен с кодом закрытия: %s', close_code)

    def receive(self, text_data=None, bytes_data=None):
        """
        Вызывается при получении сообщения от веб-сокета.
        Разбирает полученные JSON-данные, извлекает сообщение и отправляет его обратно в веб-сокет.
        """
        try:
            # Разбор полученных JSON-данных
            text_data_json = json.loads(text_data)

            # Парсинг сообщения из JSON-данных
            message = text_data_json['message']

            # Отправка полученного сообщения обратно в веб-сокет
            self.send(text_data=json.dumps({'message': message}))
            logger.info('Сообщение получено и отправлено: %s', message)
        except json.JSONDecodeError as e:
            logger.error('Ошибка декодирования JSON: %s', str(e))
        except KeyError as e:
            logger.error('KeyError при парсинге сообщения: %s', str(e))
