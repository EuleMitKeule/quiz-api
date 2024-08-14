"""Entrypoint for quiz-api application."""

import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import update
from sqlmodel import Session

from quiz_api.config import config
from quiz_api.const import API_PREFIX
from quiz_api.db import Database, db_engine
from quiz_api.log import logger
from quiz_api.models import User
from quiz_api.routers.assignment_answer_router import assignment_answer_router
from quiz_api.routers.assignment_option_router import assignment_option_router
from quiz_api.routers.assignment_question_router import assignment_question_router
from quiz_api.routers.auth_router import auth_router
from quiz_api.routers.gap_text_answer_router import gap_text_answer_router
from quiz_api.routers.gap_text_option_router import gap_text_option_router
from quiz_api.routers.gap_text_question_router import gap_text_question_router
from quiz_api.routers.gap_text_sub_question_router import gap_text_sub_question_router
from quiz_api.routers.label_router import label_router
from quiz_api.routers.multiple_choice_answer_router import multiple_choice_answer_router
from quiz_api.routers.multiple_choice_option_router import multiple_choice_option_router
from quiz_api.routers.multiple_choice_question_router import (
    multiple_choice_question_router,
)
from quiz_api.routers.open_answer_router import open_answer_router
from quiz_api.routers.open_option_router import open_option_router
from quiz_api.routers.open_question_router import open_question_router
from quiz_api.routers.quiz_router import quiz_router
from quiz_api.routers.result_router import result_router
from quiz_api.routers.single_choice_answer_router import single_choice_answer_router
from quiz_api.routers.single_choice_option_router import single_choice_option_router
from quiz_api.routers.single_choice_question_router import single_choice_question_router
from quiz_api.routers.user_router import user_router
from quiz_api.security import get_current_user, get_password_hash, get_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""

    logger.info("Starting application.")

    Database.create_db()

    try:
        Database.run_migrations()
    except Exception as e:
        logger.error(f"Error running migrations: {e}")

    test_user = get_user(config.test_username)
    test_password_hash = get_password_hash(config.test_password)

    if test_user is not None:
        test_user.hashed_password = test_password_hash

        with Session(db_engine) as session:
            session.exec(
                update(User)
                .where(User.username == config.test_username)
                .values(hashed_password=test_password_hash)
            )
            session.commit()
    else:
        test_user = User(
            username=config.test_username,
            hashed_password=test_password_hash,
            is_admin=False,
        )

        with Session(db_engine) as session:
            session.add(test_user)
            session.commit()

    admin_user = get_user(config.admin_username)
    admin_password_hash = get_password_hash(config.admin_password)

    if admin_user is not None:
        admin_user.hashed_password = admin_password_hash

        with Session(db_engine) as session:
            session.exec(
                update(User)
                .where(User.username == config.admin_username)
                .values(hashed_password=admin_password_hash)
            )
            session.commit()
    else:
        admin_user = User(
            username=config.admin_username,
            hashed_password=admin_password_hash,
            is_admin=True,
        )

        with Session(db_engine) as session:
            session.add(admin_user)
            session.commit()

    logger.info("Application started.")

    yield

    logger.info("Stopping application.")
    logger.info("Application stopped.")


app = FastAPI(title="quiz-api", lifespan=lifespan)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(
    user_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    quiz_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    result_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    single_choice_question_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    multiple_choice_question_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    single_choice_option_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    multiple_choice_option_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    open_question_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    open_option_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    assignment_question_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    assignment_option_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    gap_text_question_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    gap_text_sub_question_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    gap_text_option_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    single_choice_answer_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    multiple_choice_answer_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    open_answer_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    gap_text_answer_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    assignment_answer_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    label_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)


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
