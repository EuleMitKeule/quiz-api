"""AssignmentQuestion router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import AssignmentQuestion, AssignmentQuestionRead
from quiz_api.security import require_admin

assignment_question_router = APIRouter(
    prefix="/assignment_question", tags=["assignment_question"]
)


@assignment_question_router.get(
    "",
    response_model=list[AssignmentQuestionRead],
    operation_id="get_assignment_questions",
    dependencies=[Depends(require_admin)],
)
async def get_assignment_questions():
    """Get all assignment questions."""

    with Session(db_engine) as session:
        assignment_questions = session.exec(select(AssignmentQuestion)).all()

    return assignment_questions


@assignment_question_router.get(
    "/{assignment_question_id}",
    response_model=AssignmentQuestionRead,
    operation_id="get_assignment_question",
    dependencies=[Depends(require_admin)],
)
async def get_assignment_question(assignment_question_id: int):
    """Get an assignment question by ID."""

    with Session(db_engine) as session:
        assignment_question = session.get(AssignmentQuestion, assignment_question_id)

    return assignment_question


@assignment_question_router.post(
    "",
    response_model=AssignmentQuestionRead,
    operation_id="create_assignment_question",
    dependencies=[Depends(require_admin)],
)
async def create_assignment_question(assignment_question: AssignmentQuestion):
    """Create an assignment question."""

    with Session(db_engine) as session:
        db_assignment_question = AssignmentQuestion.model_validate(assignment_question)
        session.add(db_assignment_question)
        session.commit()
        session.refresh(db_assignment_question)

    return db_assignment_question


@assignment_question_router.put(
    "/{assignment_question_id}",
    response_model=AssignmentQuestionRead,
    operation_id="update_assignment_question",
    dependencies=[Depends(require_admin)],
)
async def update_assignment_question(
    assignment_question_id: int, assignment_question: AssignmentQuestion
):
    """Update an assignment question by ID."""

    with Session(db_engine) as session:
        db_assignment_question = session.get(AssignmentQuestion, assignment_question_id)

        db_assignment_question.title = assignment_question.title
        db_assignment_question.text = assignment_question.text
        db_assignment_question.index = assignment_question.index
        db_assignment_question.quiz_id = assignment_question.quiz_id

        session.add(db_assignment_question)
        session.commit()
        session.refresh(db_assignment_question)

    return db_assignment_question


@assignment_question_router.delete(
    "/{assignment_question_id}",
    response_model=AssignmentQuestionRead,
    operation_id="delete_assignment_question",
    dependencies=[Depends(require_admin)],
)
async def delete_assignment_question(assignment_question_id: int):
    """Delete an assignment question by ID."""

    with Session(db_engine) as session:
        assignment_question = session.get(AssignmentQuestion, assignment_question_id)
        session.delete(assignment_question)
        session.commit()

    return assignment_question
