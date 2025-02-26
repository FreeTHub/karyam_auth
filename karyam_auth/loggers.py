import os
import json
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from datetime import datetime

#  Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#  Create logs directory if it doesn't exist
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

#  Custom JSON Formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)

#  Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'json': {
            '()': JsonFormatter,  # Custom JSON formatter
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s - %(module)s - %(message)s',
        },
    },

    'handlers': {
        'console': {  # Console logging (for debugging)
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'auth_file': {  # Authentication logs
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'authentication.log'),
            'maxBytes': 5*1024*1024,  # 5 MB per file
            'backupCount': 5,  # Keep last 5 log files
            'formatter': 'json',
        },
        'utils_file': {  # Utility logs
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'utils.log'),
            'maxBytes': 5*1024*1024,
            'backupCount': 5,
            'formatter': 'json',
        },
        'error_file': {  #  Error logs (Separate file)
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10*1024*1024,  # 10 MB per file
            'backupCount': 5,
            'formatter': 'json',
        },
    },

    'loggers': {
        'authentication': {
            'handlers': ['console', 'auth_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'utils': {
            'handlers': ['console', 'utils_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {  # Django logs
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {  # Log Django errors separately
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)


# auth_logger = logging.getLogger("authentication")
# utils_logger = logging.getLogger("utils")
# error_logger = logging.getLogger("django.request")  # Logs Django errors

