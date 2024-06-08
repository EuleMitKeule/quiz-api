"""Single choice option router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    SingleChoiceOption,
    SingleChoiceOptionCreate,
    SingleChoiceOptionRead,
)
from quiz_api.security import require_admin

single_choice_option_router = APIRouter(
    prefix="/single_choice_option", tags=["single_choice_option"]
)


@single_choice_option_router.get(
    "",
    response_model=list[SingleChoiceOptionRead],
    operation_id="get_single_choice_options",
)
async def get_single_choice_options():
    """Get all single choice options."""

    with Session(db_engine) as session:
        options = session.exec(select(SingleChoiceOption)).all()

    return options


@single_choice_option_router.get(
    "/{option_id}",
    response_model=SingleChoiceOptionRead,
    operation_id="get_single_choice_option",
)
async def get_single_choice_option(option_id: int):
    """Get a single choice option by ID."""

    with Session(db_engine) as session:
        option = session.get(SingleChoiceOption, option_id)

    return option


@single_choice_option_router.post(
    "",
    response_model=SingleChoiceOptionRead,
    operation_id="create_single_choice_option",
    dependencies=[Depends(require_admin)],
)
async def create_single_choice_option(option: SingleChoiceOptionCreate):
    """Create a single choice option."""

    with Session(db_engine) as session:
        db_option = SingleChoiceOption.model_validate(option)
        session.add(db_option)
        session.commit()
        session.refresh(db_option)

    return db_option


@single_choice_option_router.put(
    "/{option_id}",
    response_model=SingleChoiceOptionRead,
    operation_id="update_single_choice_option",
    dependencies=[Depends(require_admin)],
)
async def update_single_choice_option(option_id: int, option: SingleChoiceOptionCreate):
    """Update a single choice option by ID."""

    with Session(db_engine) as session:
        db_option = session.get(SingleChoiceOption, option_id)

        db_option.text = option.text
        db_option.question_id = option.question_id
        db_option.index = option.index

        session.add(db_option)
        session.commit()
        session.refresh(db_option)

    return db_option


@single_choice_option_router.delete(
    "/{option_id}",
    response_model=int,
    operation_id="delete_single_choice_option",
    dependencies=[Depends(require_admin)],
)
async def delete_single_choice_option(option_id: int):
    """Delete a single choice option by ID."""

    with Session(db_engine) as session:
        option = session.get(SingleChoiceOption, option_id)
        session.delete(option)
        session.commit()

    return option_id
