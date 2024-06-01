"""AssignmentOption router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import AssignmentOption, AssignmentOptionRead
from quiz_api.security import require_admin

assignment_option_router = APIRouter(
    prefix="/assignment_option", tags=["assignment_option"]
)


@assignment_option_router.get(
    "",
    response_model=list[AssignmentOptionRead],
    operation_id="get_assignment_options",
    dependencies=[Depends(require_admin)],
)
async def get_assignment_options():
    """Get all assignment options."""

    with Session(db_engine) as session:
        assignment_options = session.exec(select(AssignmentOption)).all()

    return assignment_options


@assignment_option_router.get(
    "/{assignment_option_id}",
    response_model=AssignmentOptionRead,
    operation_id="get_assignment_option",
    dependencies=[Depends(require_admin)],
)
async def get_assignment_option(assignment_option_id: int):
    """Get an assignment option by ID."""

    with Session(db_engine) as session:
        assignment_option = session.get(AssignmentOption, assignment_option_id)

    return assignment_option


@assignment_option_router.post(
    "",
    response_model=AssignmentOptionRead,
    operation_id="create_assignment_option",
    dependencies=[Depends(require_admin)],
)
async def create_assignment_option(assignment_option: AssignmentOption):
    """Create an assignment option."""

    with Session(db_engine) as session:
        db_assignment_option = AssignmentOption.model_validate(assignment_option)
        session.add(db_assignment_option)
        session.commit()
        session.refresh(db_assignment_option)

    return db_assignment_option


@assignment_option_router.put(
    "/{assignment_option_id}",
    response_model=AssignmentOptionRead,
    operation_id="update_assignment_option",
    dependencies=[Depends(require_admin)],
)
async def update_assignment_option(
    assignment_option_id: int, assignment_option: AssignmentOption
):
    """Update an assignment option."""

    with Session(db_engine) as session:
        db_assignment_option = session.get(AssignmentOption, assignment_option_id)
        db_assignment_option = AssignmentOption.model_validate(
            assignment_option, db_assignment_option
        )
        session.add(db_assignment_option)
        session.commit()
        session.refresh(db_assignment_option)

    return db_assignment_option


@assignment_option_router.delete(
    "/{assignment_option_id}",
    response_model=AssignmentOptionRead,
    operation_id="delete_assignment_option",
    dependencies=[Depends(require_admin)],
)
async def delete_assignment_option(assignment_option_id: int):
    """Delete an assignment option by ID."""

    with Session(db_engine) as session:
        assignment_option = session.get(AssignmentOption, assignment_option_id)
        session.delete(assignment_option)
        session.commit()

    return assignment_option
