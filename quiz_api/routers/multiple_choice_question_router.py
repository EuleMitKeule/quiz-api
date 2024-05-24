"""Multiple choice question router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models.multiple_choice_question import (
    MultipleChoiceQuestion,
    MultipleChoiceQuestionCreate,
    MultipleChoiceQuestionRead,
)
from quiz_api.security import require_admin

multiple_choice_question_router = APIRouter(
    prefix="/multiple_choice_question", tags=["multiple_choice_question"]
)


@multiple_choice_question_router.get(
    "",
    response_model=list[MultipleChoiceQuestionRead],
    operation_id="get_multiple_choice_questions",
)
async def get_multiple_choice_questions():
    """Get all multiple choice questions."""

    with Session(db_engine) as session:
        questions = session.exec(select(MultipleChoiceQuestion)).all()

    return questions


@multiple_choice_question_router.get(
    "/{question_id}",
    response_model=MultipleChoiceQuestionRead,
    operation_id="get_multiple_choice_question",
)
async def get_multiple_choice_question(question_id: int):
    """Get a multiple choice question by ID."""

    with Session(db_engine) as session:
        question = session.get(MultipleChoiceQuestion, question_id)

    return question


@multiple_choice_question_router.post(
    "",
    response_model=MultipleChoiceQuestionCreate,
    operation_id="create_multiple_choice_question",
    dependencies=[Depends(require_admin)],
)
async def create_quiz(question: MultipleChoiceQuestionCreate):
    """Create a multiple choice question."""

    with Session(db_engine) as session:
        db_question = MultipleChoiceQuestion.model_validate(question)
        session.add(db_question)
        session.commit()

    return db_question


@multiple_choice_question_router.put(
    "/{question_id}",
    response_model=MultipleChoiceQuestionRead,
    operation_id="update_multiple_choice_question",
    dependencies=[Depends(require_admin)],
)
async def update_multiple_choice_question(
    question_id: int, question: MultipleChoiceQuestionCreate
):
    """Update a multiple choice question."""

    with Session(db_engine) as session:
        db_question = session.get(MultipleChoiceQuestion, question_id)
        db_question = MultipleChoiceQuestion.model_validate(question, db_question)
        session.commit()

    return db_question


@multiple_choice_question_router.delete(
    "/{question_id}",
    operation_id="delete_multiple_choice_question",
    dependencies=[Depends(require_admin)],
)
async def delete_multiple_choice_question(question_id: int):
    """Delete a multiple choice question."""

    with Session(db_engine) as session:
        question = session.get(MultipleChoiceQuestion, question_id)
        session.delete(question)
        session.commit()

    return {"message": "Question deleted successfully."}