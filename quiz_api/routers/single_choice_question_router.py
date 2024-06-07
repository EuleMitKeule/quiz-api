"""Single choice question router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    SingleChoiceQuestion,
    SingleChoiceQuestionCreate,
    SingleChoiceQuestionRead,
)
from quiz_api.security import require_admin

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
        questions = session.exec(select(SingleChoiceQuestion)).unique().all()

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
    dependencies=[Depends(require_admin)],
)
async def create_quiz(question: SingleChoiceQuestionCreate):
    """Create a single choice question."""

    with Session(db_engine) as session:
        db_question = SingleChoiceQuestion.model_validate(question)
        session.add(db_question)
        session.commit()

    return db_question


@single_choice_question_router.put(
    "/{question_id}",
    response_model=SingleChoiceQuestionRead,
    operation_id="update_single_choice_question",
    dependencies=[Depends(require_admin)],
)
async def update_single_choice_question(
    question_id: int, question: SingleChoiceQuestionCreate
):
    """Update a single choice question."""

    with Session(db_engine) as session:
        db_question = session.get(SingleChoiceQuestion, question_id)

        db_question.title = question.title
        db_question.text = question.text
        db_question.index = question.index
        db_question.correct_index = question.correct_index
        db_question.quiz_id = question.quiz_id

        session.add(db_question)
        session.commit()
        session.refresh(db_question)

    return db_question


@single_choice_question_router.delete(
    "/{question_id}",
    response_model=SingleChoiceQuestionRead,
    operation_id="delete_single_choice_question",
    dependencies=[Depends(require_admin)],
)
async def delete_single_choice_question(question_id: int):
    """Delete a single choice question by ID."""

    with Session(db_engine) as session:
        question = session.get(SingleChoiceQuestion, question_id)
        session.delete(question)
        session.commit()

    return question
