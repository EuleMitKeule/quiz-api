"""Multiple choice option router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import (
    MultipleChoiceOption,
    MultipleChoiceOptionCreate,
    MultipleChoiceOptionRead,
)
from quiz_api.security import require_admin

multiple_choice_option_router = APIRouter(
    prefix="/multiple_choice_option", tags=["multiple_choice_option"]
)


@multiple_choice_option_router.get(
    "",
    response_model=list[MultipleChoiceOptionRead],
    operation_id="get_multiple_choice_options",
)
async def get_multiple_choice_options():
    """Get all multiple choice options."""

    with Session(db_engine) as session:
        options = session.exec(select(MultipleChoiceOption)).all()

    return options


@multiple_choice_option_router.get(
    "/{option_id}",
    response_model=MultipleChoiceOptionRead,
    operation_id="get_multiple_choice_option",
)
async def get_multiple_choice_option(option_id: int):
    """Get a multiple choice option by ID."""

    with Session(db_engine) as session:
        option = session.get(MultipleChoiceOption, option_id)

    return option


@multiple_choice_option_router.post(
    "",
    response_model=MultipleChoiceOptionRead,
    operation_id="create_multiple_choice_option",
    dependencies=[Depends(require_admin)],
)
async def create_quiz(option: MultipleChoiceOptionCreate):
    """Create a multiple choice option."""

    with Session(db_engine) as session:
        db_option = MultipleChoiceOption.model_validate(option)
        session.add(db_option)
        session.commit()
        session.refresh(db_option)

    return db_option


@multiple_choice_option_router.put(
    "/{option_id}",
    response_model=MultipleChoiceOptionRead,
    operation_id="update_multiple_choice_option",
    dependencies=[Depends(require_admin)],
)
async def update_multiple_choice_option(
    option_id: int, option: MultipleChoiceOptionCreate
):
    """Update a multiple choice option by ID."""

    with Session(db_engine) as session:
        db_option = session.get(MultipleChoiceOption, option_id)

        db_option.text = option.text
        db_option.is_correct = option.is_correct
        db_option.question_id = option.question_id
        db_option.index = option.index

        session.add(db_option)
        session.commit()
        session.refresh(db_option)

    return db_option


@multiple_choice_option_router.delete(
    "/{option_id}",
    response_model=int,
    operation_id="delete_multiple_choice_option",
    dependencies=[Depends(require_admin)],
)
async def delete_multiple_choice_option(option_id: int):
    """Delete a multiple choice option by ID."""

    with Session(db_engine) as session:
        option = session.get(MultipleChoiceOption, option_id)
        session.delete(option)
        session.commit()

    return option_id
