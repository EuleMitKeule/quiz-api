"""SingleChoiceAnswer router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    SingleChoiceAnswer,
    SingleChoiceAnswerCreate,
    SingleChoiceAnswerRead,
)
from quiz_api.security import require_admin

single_choice_answer_router = APIRouter(
    prefix="/single_choice_answer", tags=["single_choice_answer"]
)


@single_choice_answer_router.get(
    "",
    response_model=list[SingleChoiceAnswerRead],
    operation_id="get_single_choice_answers",
)
async def get_single_choice_answers():
    """Get all single choice answers."""

    with Session(db_engine) as session:
        answers = session.exec(select(SingleChoiceAnswer)).all()

    return answers


@single_choice_answer_router.get(
    "/{answer_id}",
    response_model=SingleChoiceAnswerRead,
    operation_id="get_single_choice_answer",
)
async def get_single_choice_answer(answer_id: int):
    """Get a single choice answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(SingleChoiceAnswer, answer_id)

    return answer


@single_choice_answer_router.post(
    "",
    response_model=SingleChoiceAnswerCreate,
    operation_id="create_single_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def create_single_choice_answer(answer: SingleChoiceAnswerCreate):
    """Create a single choice answer."""

    with Session(db_engine) as session:
        db_answer = SingleChoiceAnswer.model_validate(answer)
        session.add(db_answer)
        session.commit()

    return db_answer


@single_choice_answer_router.put(
    "/{answer_id}",
    response_model=SingleChoiceAnswerRead,
    operation_id="update_single_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def update_single_choice_answer(answer_id: int, answer: SingleChoiceAnswerCreate):
    """Update a single choice answer."""

    with Session(db_engine) as session:
        db_answer = session.get(SingleChoiceAnswer, answer_id)

        db_answer.question_id = answer.question_id
        db_answer.result_id = answer.result_id
        db_answer.selected_index = answer.selected_index

        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@single_choice_answer_router.delete(
    "/{answer_id}",
    response_model=SingleChoiceAnswerRead,
    operation_id="delete_single_choice_answer",
    dependencies=[Depends(require_admin)],
)
async def delete_single_choice_answer(answer_id: int):
    """Delete a single choice answer."""

    with Session(db_engine) as session:
        answer = session.get(SingleChoiceAnswer, answer_id)
        session.delete(answer)
        session.commit()

    return answer
