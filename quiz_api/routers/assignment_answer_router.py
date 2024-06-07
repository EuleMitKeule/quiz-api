"""AssignmentAnswer router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    AssignmentAnswer,
    AssignmentAnswerCreate,
    AssignmentAnswerRead,
)
from quiz_api.security import require_admin

assignment_answer_router = APIRouter(
    prefix="/assignment_answer", tags=["assignment_answer"]
)


@assignment_answer_router.get(
    "",
    response_model=list[AssignmentAnswerRead],
    operation_id="get_assignment_answers",
)
async def get_assignment_answers():
    """Get all assignment answers."""

    with Session(db_engine) as session:
        answers = session.exec(select(AssignmentAnswer)).all()

    return answers


@assignment_answer_router.get(
    "/{answer_id}",
    response_model=AssignmentAnswerRead,
    operation_id="get_assignment_answer",
)
async def get_assignment_answer(answer_id: int):
    """Get an assignment answer by ID."""

    with Session(db_engine) as session:
        answer = session.get(AssignmentAnswer, answer_id)

    return answer


@assignment_answer_router.post(
    "",
    response_model=AssignmentAnswerCreate,
    operation_id="create_assignment_answer",
    dependencies=[Depends(require_admin)],
)
async def create_assignment_answer(answer: AssignmentAnswerCreate):
    """Create an assignment answer."""

    with Session(db_engine) as session:
        db_answer = AssignmentAnswer.model_validate(answer)
        session.add(db_answer)
        session.commit()

    return db_answer


@assignment_answer_router.put(
    "/{answer_id}",
    response_model=AssignmentAnswerCreate,
    operation_id="update_assignment_answer",
    dependencies=[Depends(require_admin)],
)
async def update_assignment_answer(answer_id: int, answer: AssignmentAnswerCreate):
    """Update an assignment answer."""

    with Session(db_engine) as session:
        db_answer = session.get(AssignmentAnswer, answer_id)

        db_answer.question_id = answer.question_id
        db_answer.result_id = answer.result_id
        db_answer.selected_indices = answer.selected_indices

        session.add(db_answer)
        session.commit()
        session.refresh(db_answer)

    return db_answer


@assignment_answer_router.delete(
    "/{answer_id}",
    response_model=AssignmentAnswerRead,
    operation_id="delete_assignment_answer",
    dependencies=[Depends(require_admin)],
)
async def delete_assignment_answer(answer_id: int):
    """Delete an assignment answer."""

    with Session(db_engine) as session:
        answer = session.get(AssignmentAnswer, answer_id)
        session.delete(answer)
        session.commit()

    return answer
