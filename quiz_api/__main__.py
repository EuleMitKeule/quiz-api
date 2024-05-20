"""Entrypoint for quiz-api application."""

import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from quiz_api.config import config
from quiz_api.const import API_PREFIX
from quiz_api.db import Database
from quiz_api.log import logger
from quiz_api.routers.quiz_router import quiz_router
from quiz_api.routers.single_choice_question_router import single_choice_question_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""

    logger.info("Starting application.")

    Database.create_db()

    logger.info("Application started.")

    yield

    logger.info("Stopping application.")
    logger.info("Application stopped.")


app = FastAPI(title="quiz-api", lifespan=lifespan)

app.include_router(quiz_router, prefix=API_PREFIX)
app.include_router(single_choice_question_router, prefix=API_PREFIX)


def start():
    """Start the application."""

    try:
        uvicorn.run(
            app,
            host=config.host,
            port=config.port,
            log_level="warning",
        )
    except KeyboardInterrupt:
        pass


def generate_openapi():
    """Generate the OpenAPI schema."""

    with open("openapi.json", "w", encoding="utf-8") as openapi_file:
        dump = json.dumps(app.openapi(), indent=2)
        openapi_file.write(dump)


if __name__ == "__main__":
    start()
