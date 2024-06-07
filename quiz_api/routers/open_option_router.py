"""OpenOption router."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import OpenOption, OpenOptionRead
from quiz_api.security import require_admin

open_option_router = APIRouter(prefix="/open_option", tags=["open_option"])


@open_option_router.get(
    "",
    response_model=list[OpenOptionRead],
    operation_id="get_open_options",
    dependencies=[Depends(require_admin)],
)
async def get_open_options():
    """Get all open options."""

    with Session(db_engine) as session:
        open_options = session.exec(select(OpenOption)).all()

    return open_options


@open_option_router.get(
    "/{open_option_id}",
    response_model=OpenOptionRead,
    operation_id="get_open_option",
    dependencies=[Depends(require_admin)],
)
async def get_open_option(open_option_id: int):
    """Get an open option by ID."""

    with Session(db_engine) as session:
        open_option = session.get(OpenOption, open_option_id)

    return open_option


@open_option_router.post(
    "",
    response_model=OpenOptionRead,
    operation_id="create_open_option",
    dependencies=[Depends(require_admin)],
)
async def create_open_option(open_option: OpenOption):
    """Create an open option."""

    with Session(db_engine) as session:
        db_open_option = OpenOption.model_validate(open_option)
        session.add(db_open_option)
        session.commit()
        session.refresh(db_open_option)

    return db_open_option


@open_option_router.put(
    "/{open_option_id}",
    response_model=OpenOptionRead,
    operation_id="update_open_option",
    dependencies=[Depends(require_admin)],
)
async def update_open_option(open_option_id: int, open_option: OpenOption):
    """Update an open option."""

    with Session(db_engine) as session:
        db_open_option = session.get(OpenOption, open_option_id)

        db_open_option.text = open_option.text
        db_open_option.index = open_option.index
        db_open_option.question_id = open_option.question_id

        session.add(db_open_option)
        session.commit()
        session.refresh(db_open_option)

    return db_open_option


@open_option_router.delete(
    "/{open_option_id}",
    response_model=OpenOptionRead,
    operation_id="delete_open_option",
    dependencies=[Depends(require_admin)],
)
async def delete_open_option(open_option_id: int):
    """Delete an open option."""

    with Session(db_engine) as session:
        open_option = session.get(OpenOption, open_option_id)
        session.delete(open_option)
        session.commit()

    return open_option
