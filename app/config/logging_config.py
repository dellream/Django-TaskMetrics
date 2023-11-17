from logging.config import dictConfig

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logging.log',
            'formatter': 'standart',
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 10,
            'level': 'WARNING',  # Установите уровень на WARNING, чтобы записывать только WARNING и выше
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standart',
            'level': 'INFO',  # Установите уровень на DEBUG, чтобы выводить все уровни в консоль
        },
    },
    'root': {
        'handlers': ['rotating_file', 'console'],
        'level': 'INFO',
    },
}

dictConfig(LOGGING)