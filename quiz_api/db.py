"""Database for the quiz-api application."""

from alembic import command
from alembic.config import Config
from sqlmodel import Session, SQLModel, create_engine

from quiz_api.config import config
from quiz_api.log import logger

db_engine = create_engine(config.db_url)


class Database:
    @staticmethod
    def create_db():
        """Create the database tables."""

        logger.info("Creating database tables.")

        with Session(db_engine) as session:
            SQLModel.metadata.create_all(db_engine)
            session.commit()

    @staticmethod
    def drop_db():
        """Drop the database tables."""

        logger.info("Dropping database tables.")

        with Session(db_engine) as session:
            SQLModel.metadata.drop_all(db_engine)
            session.commit()

    @staticmethod
    def run_migrations():
        """Run database migrations."""

        logger.info("Running database migrations.")

        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", "quiz_api/migrations")
        alembic_cfg.set_main_option("sqlalchemy.url", config.db_url)
        command.upgrade(alembic_cfg, "head")
