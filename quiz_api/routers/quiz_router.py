"""Quiz router."""

from fastapi import APIRouter
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models.quiz import Quiz, QuizCreate, QuizRead

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
    response_model=QuizCreate,
    operation_id="create_quiz",
)
async def create_quiz(quiz: QuizCreate):
    """Create a quiz."""

    with Session(db_engine) as session:
        db_quiz = Quiz.model_validate(quiz)
        session.add(db_quiz)
        session.commit()

    return db_quiz
