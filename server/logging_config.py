import sys
from uvicorn.logging import DefaultFormatter


log_config = {
    "version":  1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": DefaultFormatter,
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["default"],
    },
    "loggers": {
        "fastapi": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
        "uvicorn": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": True,
        },
    },
}