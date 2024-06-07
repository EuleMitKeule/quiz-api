"""Logging configuration for the quiz-api application."""

import logging
from logging import config as logging_config

from quiz_api.config import config
from quiz_api.const import LOGGING_CONFIG

LOGGING_CONFIG["handlers"]["file"]["filename"] = config.log_path
# LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = config.log_level
# LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = config.log_level
# LOGGING_CONFIG["loggers"]["quiz_api"]["level"] = config.log_level

logging_config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("quiz_api")
