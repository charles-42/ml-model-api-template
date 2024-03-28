import logging.config
import os

log_directory = "./api/logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

def setup_logging_config():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            },
            "simple": {
                "format": "%(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"{log_directory}/api.log",
                "maxBytes": 10485760,
                "backupCount": 3,
                "formatter": "standard",
                "level": "INFO",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "my_application": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    })
