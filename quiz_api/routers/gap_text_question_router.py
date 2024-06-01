"""GapTextQuestion router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import GapTextQuestion, GapTextQuestionRead
from quiz_api.security import require_admin

gap_text_question_router = APIRouter(
    prefix="/gap_text_question", tags=["gap_text_question"]
)


@gap_text_question_router.get(
    "",
    response_model=list[GapTextQuestionRead],
    operation_id="get_gap_text_questions",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_questions():
    """Get all gap text questions."""

    with Session(db_engine) as session:
        gap_text_questions = session.exec(select(GapTextQuestion)).all()

    return gap_text_questions


@gap_text_question_router.get(
    "/{gap_text_question_id}",
    response_model=GapTextQuestionRead,
    operation_id="get_gap_text_question",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_question(gap_text_question_id: int):
    """Get a gap text question by ID."""

    with Session(db_engine) as session:
        gap_text_question = session.get(GapTextQuestion, gap_text_question_id)

    return gap_text_question


@gap_text_question_router.post(
    "",
    response_model=GapTextQuestionRead,
    operation_id="create_gap_text_question",
    dependencies=[Depends(require_admin)],
)
async def create_gap_text_question(gap_text_question: GapTextQuestion):
    """Create a gap text question."""

    with Session(db_engine) as session:
        db_gap_text_question = GapTextQuestion.model_validate(gap_text_question)
        session.add(db_gap_text_question)
        session.commit()
        session.refresh(db_gap_text_question)

    return db_gap_text_question


@gap_text_question_router.put(
    "/{gap_text_question_id}",
    response_model=GapTextQuestionRead,
    operation_id="update_gap_text_question",
    dependencies=[Depends(require_admin)],
)
async def update_gap_text_question(
    gap_text_question_id: int, gap_text_question: GapTextQuestion
):
    """Update a gap text question by ID."""

    with Session(db_engine) as session:
        db_gap_text_question = session.get(GapTextQuestion, gap_text_question_id)
        db_gap_text_question.text = gap_text_question.text
        db_gap_text_question.gaps = gap_text_question.gaps
        db_gap_text_question.correct_answers = gap_text_question.correct_answers
        session.add(db_gap_text_question)
        session.commit()
        session.refresh(db_gap_text_question)

    return db_gap_text_question


@gap_text_question_router.delete(
    "/{gap_text_question_id}",
    response_model=GapTextQuestionRead,
    operation_id="delete_gap_text_question",
    dependencies=[Depends(require_admin)],
)
async def delete_gap_text_question(gap_text_question_id: int):
    """Delete a gap text question by ID."""

    with Session(db_engine) as session:
        gap_text_question = session.get(GapTextQuestion, gap_text_question_id)
        session.delete(gap_text_question)
        session.commit()

    return gap_text_question
