import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY_ENV = os.environ.get('SECRET_KEY_ENV')

# Переменные для подключения к Postgresql
DB_HOST = os.environ.get('DB_HOST')
# DB_DOCKER_HOST = os.environ.get('DB_DOCKER_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Пути
LOCALHOST_URL = 'http://localhost:8000/'
HOME_URL = LOCALHOST_URL
LOGIN_URL = LOCALHOST_URL + 'account/login/'
REGISTER_URL = LOCALHOST_URL + 'account/register/'

if __name__ == '__main__':
    print(DB_HOST)
