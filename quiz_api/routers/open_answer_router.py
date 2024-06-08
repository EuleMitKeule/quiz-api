"""OpenAnswer router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    OpenAnswer,
    OpenAnswerCreate,
    OpenAnswerRead,
)
from quiz_api.security import require_admin

open_answer_router = APIRouter(prefix="/open_answer", tags=["open_answer"])


@open_answer_router.get(
    "",
    response_model=list[OpenAnswerRead],
    operation_id="get_open_answers",
)
async def get_open_answers():
    """Get all open answers."""

    with Session(db_engine) as session:
        answers = session.exec(select(OpenAnswer)).all()

    return answers


@open_answer_router.get(
    "/{answer_id}",
    response_model=OpenAnswerRead,
    operation_id="get_open_answer",
)
async def get_open_answer(answer_id: int):
    """Get an open answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(OpenAnswer, answer_id)

    return answer


@open_answer_router.post(
    "",
    response_model=OpenAnswerRead,
    operation_id="create_open_answer",
    dependencies=[Depends(require_admin)],
)
async def create_open_answer(answer: OpenAnswerCreate):
    """Create an open answer."""

    with Session(db_engine) as session:
        db_answer = OpenAnswer.model_validate(answer)
        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@open_answer_router.put(
    "/{answer_id}",
    response_model=OpenAnswerRead,
    operation_id="update_open_answer",
    dependencies=[Depends(require_admin)],
)
async def update_open_answer(answer_id: int, answer: OpenAnswerCreate):
    """Update an open answer."""

    with Session(db_engine) as session:
        db_answer = session.get(OpenAnswer, answer_id)

        db_answer.question_id = answer.question_id
        db_answer.result_id = answer.result_id
        db_answer.text = answer.text

        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@open_answer_router.delete(
    "/{answer_id}",
    response_model=int,
    operation_id="delete_open_answer",
    dependencies=[Depends(require_admin)],
)
async def delete_open_answer(answer_id: int):
    """Delete an open answer."""

    with Session(db_engine) as session:
        answer = session.get(OpenAnswer, answer_id)
        session.delete(answer)
        session.commit()

    return answer_id
