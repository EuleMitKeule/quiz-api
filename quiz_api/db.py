"""Database for the quiz-api application."""

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
