from typing import Any
from pathlib import Path

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
            'filename': str(Path(__file__).resolve().parent.parent.parent.parent / 'logs' / 'idk.log'),
            'formatter': 'custom_style',
            'level': 'DEBUG'
        }
    },
    'root': {
        'handlers': ['file_worker'],
        'level': 'DEBUG'
    }
}

if __name__ == "__main__":
    print(Path(__file__).resolve().parent.parent.parent.parent / 'idk.log' )