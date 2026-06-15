from typing import Any

LOGGING_CONFIG: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom_style': {
            'format': '[%(asctime)s] [%(levelname)s] "%(message)s" [%(filename)s:%(funcName)s:%(lineno)d]',
            'datefmt': '%d/%m/%y %H:%M:%S'
        }
    },
    'handlers': {
        'file_worker': {
            'mode': 'w',
            'class': 'logging.FileHandler',
            'filename': 'logs/idk_debug.log',
            'formatter': 'custom_style',
            'level': 'DEBUG'
        }
    },
    'root': {
        'handlers': ['file_worker'],
        'level': 'DEBUG'
    }
}