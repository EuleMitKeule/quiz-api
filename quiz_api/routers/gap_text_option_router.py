"""GapTextOption router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import GapTextOption, GapTextOptionRead
from quiz_api.security import require_admin

gap_text_option_router = APIRouter(prefix="/gap_text_option", tags=["gap_text_option"])


@gap_text_option_router.get(
    "",
    response_model=list[GapTextOptionRead],
    operation_id="get_gap_text_options",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_options():
    """Get all gap text options."""

    with Session(db_engine) as session:
        gap_text_options = session.exec(select(GapTextOption)).all()

    return gap_text_options


@gap_text_option_router.get(
    "/{gap_text_option_id}",
    response_model=GapTextOptionRead,
    operation_id="get_gap_text_option",
    dependencies=[Depends(require_admin)],
)
async def get_gap_text_option(gap_text_option_id: int):
    """Get a gap text option by ID."""

    with Session(db_engine) as session:
        gap_text_option = session.get(GapTextOption, gap_text_option_id)

    return gap_text_option


@gap_text_option_router.post(
    "",
    response_model=GapTextOptionRead,
    operation_id="create_gap_text_option",
    dependencies=[Depends(require_admin)],
)
async def create_gap_text_option(gap_text_option: GapTextOption):
    """Create a gap text option."""

    with Session(db_engine) as session:
        db_gap_text_option = GapTextOption.model_validate(gap_text_option)
        session.add(db_gap_text_option)
        session.commit()
        session.refresh(db_gap_text_option)

    return db_gap_text_option


@gap_text_option_router.put(
    "/{gap_text_option_id}",
    response_model=GapTextOptionRead,
    operation_id="update_gap_text_option",
    dependencies=[Depends(require_admin)],
)
async def update_gap_text_option(
    gap_text_option_id: int, gap_text_option: GapTextOption
):
    """Update a gap text option by ID."""

    with Session(db_engine) as session:
        db_gap_text_option = session.get(GapTextOption, gap_text_option_id)

        db_gap_text_option.text = gap_text_option.text
        db_gap_text_option.index = gap_text_option.index
        db_gap_text_option.sub_question_id = gap_text_option.sub_question_id

        session.add(db_gap_text_option)
        session.commit()
        session.refresh(db_gap_text_option)

    return db_gap_text_option


@gap_text_option_router.delete(
    "/{gap_text_option_id}",
    response_model=int,
    operation_id="delete_gap_text_option",
    dependencies=[Depends(require_admin)],
)
async def delete_gap_text_option(gap_text_option_id: int):
    """Delete a gap text option by ID."""

    with Session(db_engine) as session:
        gap_text_option = session.get(GapTextOption, gap_text_option_id)
        session.delete(gap_text_option)
        session.commit()

    return gap_text_option_id
