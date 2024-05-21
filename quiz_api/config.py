"""Configuration for the quiz-api application."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

from quiz_api.const import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_DB_URL,
    DEFAULT_DEBUG,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_PATH,
    DEFAULT_PORT,
)


class Config(BaseModel):
    """The main config class."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    debug: bool = DEFAULT_DEBUG
    log_level: str = DEFAULT_LOG_LEVEL
    log_path: Path = DEFAULT_LOG_PATH
    db_url: str = DEFAULT_DB_URL
    secret_key: str
    admin_username: str
    admin_password: str
    test_username: str
    test_password: str

    @classmethod
    def from_file(cls, config_path: str):
        """Load the config from a file."""

        with open(config_path, "r", encoding="utf-8") as config_file:
            config_dict: dict = yaml.safe_load(config_file)

        config = cls.model_validate(config_dict)
        return config

    @classmethod
    def with_location(cls, path: Path):
        """Create default config with base location."""

        config = Config()
        config.db_url = f"sqlite:///{path}/quiz-api.db"
        config.log_path = path / DEFAULT_LOG_PATH

        return config


load_dotenv()

config_path: Path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

if config_path.exists():
    config = Config.from_file(config_path)
else:
    config_base_path = config_path.parent
    config = Config.with_location(config_base_path)
