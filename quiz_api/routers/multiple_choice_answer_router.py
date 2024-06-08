"""MultipleChoiceAnswer router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    MultipleChoiceAnswer,
    MultipleChoiceAnswerCreate,
    MultipleChoiceAnswerRead,
)
from quiz_api.security import require_admin

multiple_choice_answer_router = APIRouter(
    prefix="/multiple_choice_answer", tags=["multiple_choice_answer"]
)


@multiple_choice_answer_router.get(
    "",
    response_model=list[MultipleChoiceAnswerRead],
    operation_id="get_multiple_choice_answers",
)
async def get_multiple_choice_answers():
    """Get all multiple choice answers."""

    with Session(db_engine) as session:
        answers = session.exec(select(MultipleChoiceAnswer)).all()

    return answers


@multiple_choice_answer_router.get(
    "/{answer_id}",
    response_model=MultipleChoiceAnswerRead,
    operation_id="get_multiple_choice_answer",
)
async def get_multiple_choice_answer(answer_id: int):
    """Get a multiple choice answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(MultipleChoiceAnswer, answer_id)

    return answer


@multiple_choice_answer_router.post(
    "",
    response_model=MultipleChoiceAnswerRead,
    operation_id="create_multiple_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def create_multiple_choice_answer(answer: MultipleChoiceAnswerCreate):
    """Create a multiple choice answer."""

    with Session(db_engine) as session:
        db_answer = MultipleChoiceAnswer.model_validate(answer)
        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@multiple_choice_answer_router.put(
    "/{answer_id}",
    response_model=MultipleChoiceAnswerRead,
    operation_id="update_multiple_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def update_multiple_choice_answer(
    answer_id: int, answer: MultipleChoiceAnswerCreate
):
    """Update a multiple choice answer."""

    with Session(db_engine) as session:
        db_answer = session.get(MultipleChoiceAnswer, answer_id)

        db_answer.question_id = answer.question_id
        db_answer.result_id = answer.result_id
        db_answer.selected_indices = answer.selected_indices

        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@multiple_choice_answer_router.delete(
    "/{answer_id}",
    response_model=int,
    operation_id="delete_multiple_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def delete_multiple_choice_answer(answer_id: int):
    """Delete a multiple choice answer."""

    with Session(db_engine) as session:
        answer = session.get(MultipleChoiceAnswer, answer_id)
        session.delete(answer)
        session.commit()

    return answer_id
