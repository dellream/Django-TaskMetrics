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
        },
    },
    'root': {
        'handlers': ['rotating_file'],
        'level': 'WARNING',
    },
}

dictConfig(LOGGING)
