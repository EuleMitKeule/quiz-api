"""GapTextSubQuestion router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import GapTextSubQuestion, GapTextSubQuestionRead
from quiz_api.security import require_admin

gap_text_sub_question_router = APIRouter(
    prefix="/gap_text_sub_question", tags=["gap_text_sub_question"]
)


@gap_text_sub_question_router.get(
    "",
    response_model=list[GapTextSubQuestionRead],
    operation_id="get_gap_text_sub_questions",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_sub_questions():
    """Get all gap text sub questions."""

    with Session(db_engine) as session:
        gap_text_sub_questions = session.exec(select(GapTextSubQuestion)).all()

    return gap_text_sub_questions


@gap_text_sub_question_router.get(
    "/{gap_text_sub_question_id}",
    response_model=GapTextSubQuestionRead,
    operation_id="get_gap_text_sub_question",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_sub_question(gap_text_sub_question_id: int):
    """Get a gap text sub question by ID."""

    with Session(db_engine) as session:
        gap_text_sub_question = session.get(
            GapTextSubQuestion, gap_text_sub_question_id
        )

    return gap_text_sub_question


@gap_text_sub_question_router.post(
    "",
    response_model=GapTextSubQuestionRead,
    operation_id="create_gap_text_sub_question",
    dependencies=[Depends(require_admin)],
)
async def create_gap_text_sub_question(gap_text_sub_question: GapTextSubQuestion):
    """Create a gap text sub question."""

    with Session(db_engine) as session:
        db_gap_text_sub_question = GapTextSubQuestion.model_validate(
            gap_text_sub_question
        )
        session.add(db_gap_text_sub_question)
        session.commit()
        session.refresh(db_gap_text_sub_question)

    return db_gap_text_sub_question


@gap_text_sub_question_router.put(
    "/{gap_text_sub_question_id}",
    response_model=GapTextSubQuestionRead,
    operation_id="update_gap_text_sub_question",
    dependencies=[Depends(require_admin)],
)
async def update_gap_text_sub_question(
    gap_text_sub_question_id: int, gap_text_sub_question: GapTextSubQuestion
):
    """Update a gap text sub question by ID."""

    with Session(db_engine) as session:
        db_gap_text_sub_question = session.get(
            GapTextSubQuestion, gap_text_sub_question_id
        )
        db_gap_text_sub_question = GapTextSubQuestion.model_validate(
            gap_text_sub_question, db_gap_text_sub_question
        )
        session.add(db_gap_text_sub_question)
        session.commit()
        session.refresh(db_gap_text_sub_question)

    return db_gap_text_sub_question
