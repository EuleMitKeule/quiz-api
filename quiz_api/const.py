"""Constants for the quiz-api application."""

from enum import StrEnum

API_PREFIX = "/api"

DEFAULT_CONFIG_PATH = "config.yml"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000
DEFAULT_DEBUG = True
DEFAULT_LOG_PATH = "quiz-api.log"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_DB_URL = "sqlite:///quiz-api.db"

CRYPT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class QuestionDifficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)-25s %(name)-30s %(levelname)-8s %(message)s",
        },
        "file": {
            "format": "%(asctime)-25s %(name)-30s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "file",
            "class": "logging.FileHandler",
            "filename": "quiz-api.log",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default", "file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["access", "file"],
            "propagate": False,
        },
        "quiz_api": {
            "level": "INFO",
            "handlers": ["default", "file"],
            "propagate": False,
        },
    },
}
