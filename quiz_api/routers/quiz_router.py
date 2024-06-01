"""Quiz router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Quiz, QuizCreate, QuizRead
from quiz_api.security import require_admin

quiz_router = APIRouter(prefix="/quiz", tags=["quiz"])


@quiz_router.get(
    "",
    response_model=list[QuizRead],
    operation_id="get_quizzes",
)
async def get_quizzes():
    """Get all quizzes."""

    with Session(db_engine) as session:
        quizzes = session.exec(select(Quiz)).all()

    return quizzes


@quiz_router.get(
    "/{quiz_id}",
    response_model=QuizRead,
    operation_id="get_quiz",
)
async def get_quiz(quiz_id: int):
    """Get a quiz by ID."""

    with Session(db_engine) as session:
        quiz = session.get(Quiz, quiz_id)

    return quiz


@quiz_router.post(
    "",
    response_model=QuizRead,
    operation_id="create_quiz",
    dependencies=[Depends(require_admin)],
)
async def create_quiz(quiz: QuizCreate):
    """Create a quiz."""

    with Session(db_engine) as session:
        db_quiz = Quiz.model_validate(quiz)
        session.add(db_quiz)
        session.commit()
        session.refresh(db_quiz)

    return db_quiz


@quiz_router.put(
    "/{quiz_id}",
    response_model=QuizRead,
    operation_id="update_quiz",
    dependencies=[Depends(require_admin)],
)
async def update_quiz(quiz_id: int, quiz: QuizCreate):
    """Update a quiz by ID."""

    with Session(db_engine) as session:
        db_quiz = session.get(Quiz, quiz_id)
        db_quiz = Quiz.model_validate(quiz, db_quiz)
        session.add(db_quiz)
        session.commit()
        session.refresh(db_quiz)

    return db_quiz


@quiz_router.delete(
    "/{quiz_id}",
    response_model=QuizRead,
    operation_id="delete_quiz",
    dependencies=[Depends(require_admin)],
)
async def delete_quiz(quiz_id: int):
    """Delete a quiz by ID."""

    with Session(db_engine) as session:
        quiz = session.get(Quiz, quiz_id)
        session.delete(quiz)
        session.commit()

    return quiz
