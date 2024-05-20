"""Single choice question router."""

from fastapi import APIRouter
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models.single_choice_question import (
    SingleChoiceQuestion,
    SingleChoiceQuestionCreate,
    SingleChoiceQuestionRead,
)

single_choice_question_router = APIRouter(
    prefix="/single_choice_question", tags=["single_choice_question"]
)


@single_choice_question_router.get(
    "",
    response_model=list[SingleChoiceQuestionRead],
    operation_id="get_single_choice_questions",
)
async def get_single_choice_questions():
    """Get all single choice questions."""

    with Session(db_engine) as session:
        questions = session.exec(select(SingleChoiceQuestion)).all()

    return questions


@single_choice_question_router.get(
    "/{question_id}",
    response_model=SingleChoiceQuestionRead,
    operation_id="get_single_choice_question",
)
async def get_single_choice_question(question_id: int):
    """Get a single choice question by ID."""

    with Session(db_engine) as session:
        question = session.get(SingleChoiceQuestion, question_id)

    return question


@single_choice_question_router.post(
    "",
    response_model=SingleChoiceQuestionCreate,
    operation_id="create_single_choice_question",
)
async def create_quiz(question: SingleChoiceQuestionCreate):
    """Create a single choice question."""

    with Session(db_engine) as session:
        db_question = SingleChoiceQuestion.model_validate(question)
        session.add(db_question)
        session.commit()

    return db_question
