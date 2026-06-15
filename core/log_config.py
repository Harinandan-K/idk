from typing import Any

LOGGING_CONFIG: dict[str, Any] = {
    'version': 1,
    'formatters': {
        'custom_style': {
            'format': '[%(levelname)s] [%(filename)s] "%(message)s" [Line No: %(lineno)d by %(name)s]'
        }
    },
    'handlers': {
        'file_worker': {
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