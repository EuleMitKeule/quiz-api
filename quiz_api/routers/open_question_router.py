"""OpenQuestion router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import OpenQuestion, OpenQuestionRead
from quiz_api.security import require_admin

open_question_router = APIRouter(prefix="/open_question", tags=["open_question"])


@open_question_router.get(
    "",
    response_model=list[OpenQuestionRead],
    operation_id="get_open_questions",
)
async def get_open_questions():
    """Get all open questions."""

    with Session(db_engine) as session:
        open_questions = session.exec(select(OpenQuestion)).all()

    return open_questions


@open_question_router.get(
    "/{open_question_id}",
    response_model=OpenQuestionRead,
    operation_id="get_open_question",
)
async def get_open_question(open_question_id: int):
    """Get an open question by ID."""

    with Session(db_engine) as session:
        open_question = session.get(OpenQuestion, open_question_id)

    return open_question


@open_question_router.post(
    "",
    response_model=OpenQuestionRead,
    operation_id="create_open_question",
    dependencies=[Depends(require_admin)],
)
async def create_open_question(open_question: OpenQuestion):
    """Create an open question."""

    with Session(db_engine) as session:
        db_open_question = OpenQuestion.model_validate(open_question)
        session.add(db_open_question)
        session.commit()
        session.refresh(db_open_question)

    return db_open_question


@open_question_router.put(
    "/{open_question_id}",
    response_model=OpenQuestionRead,
    operation_id="update_open_question",
    dependencies=[Depends(require_admin)],
)
async def update_open_question(open_question_id: int, open_question: OpenQuestion):
    """Update an open question by ID."""

    with Session(db_engine) as session:
        db_open_question = session.get(OpenQuestion, open_question_id)

        db_open_question.title = open_question.title
        db_open_question.text = open_question.text
        db_open_question.index = open_question.index
        db_open_question.quiz_id = open_question.quiz_id

        session.add(db_open_question)
        session.commit()
        session.refresh(db_open_question)

    return db_open_question


@open_question_router.delete(
    "/{open_question_id}",
    response_model=OpenQuestionRead,
    operation_id="delete_open_question",
    dependencies=[Depends(require_admin)],
)
async def delete_open_question(open_question_id: int):
    """Delete an open question by ID."""

    with Session(db_engine) as session:
        open_question = session.get(OpenQuestion, open_question_id)
        session.delete(open_question)
        session.commit()

    return open_question
