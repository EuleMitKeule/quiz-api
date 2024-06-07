"""GapTextAnswer router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    GapTextAnswer,
    GapTextAnswerCreate,
    GapTextAnswerRead,
)
from quiz_api.security import require_admin

gap_text_answer_router = APIRouter(prefix="/gap_text_answer", tags=["gap_text_answer"])


@gap_text_answer_router.get(
    "",
    response_model=list[GapTextAnswerRead],
    operation_id="get_gap_text_answers",
)
async def get_gap_text_answers():
    """Get all gap text answers."""

    with Session(db_engine) as session:
        answers = session.exec(select(GapTextAnswer)).all()

    return answers


@gap_text_answer_router.get(
    "/{answer_id}",
    response_model=GapTextAnswerRead,
    operation_id="get_gap_text_answer",
)
async def get_gap_text_answer(answer_id: int):
    """Get a gap text answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(GapTextAnswer, answer_id)

    return answer


@gap_text_answer_router.post(
    "",
    response_model=GapTextAnswerCreate,
    operation_id="create_gap_text_answer",
    dependencies=[Depends(require_admin)],
)
async def create_gap_text_answer(answer: GapTextAnswerCreate):
    """Create a gap text answer."""

    with Session(db_engine) as session:
        db_answer = GapTextAnswer.model_validate(answer)
        session.add(db_answer)
        session.commit()

    return db_answer


@gap_text_answer_router.put(
    "/{answer_id}",
    response_model=GapTextAnswerCreate,
    operation_id="update_gap_text_answer",
    dependencies=[Depends(require_admin)],
)
async def update_gap_text_answer(answer_id: int, answer: GapTextAnswerCreate):
    """Update a gap text answer by ID."""

    with Session(db_engine) as session:
        db_answer = session.get(GapTextAnswer, answer_id)

        db_answer.question_id = answer.question_id
        db_answer.result_id = answer.result_id
        db_answer.selected_indices = answer.selected_indices

        session.add(db_answer)
        session.commit()

    return db_answer


@gap_text_answer_router.delete(
    "/{answer_id}",
    response_model=GapTextAnswerRead,
    operation_id="delete_gap_text_answer",
    dependencies=[Depends(require_admin)],
)
async def delete_gap_text_answer(answer_id: int):
    """Delete a gap text answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(GapTextAnswer, answer_id)
        session.delete(answer)
        session.commit()

    return answer
