"""Result router."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Result, ResultCreate, ResultRead, User
from quiz_api.security import get_current_user

result_router = APIRouter(prefix="/result", tags=["result"])


@result_router.post(
    "",
    response_model=ResultRead,
    operation_id="create_result",
)
async def create_result(
    result: ResultCreate,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a result for the current user."""

    db_result = Result(
        user_id=current_user.id,
        quiz_id=result.quiz_id,
        score=result.score,
        total=result.total,
    )

    with Session(db_engine) as session:
        session.add(db_result)
        session.commit()
        session.refresh(db_result)

    return db_result


@result_router.get(
    "",
    response_model=list[ResultRead],
    operation_id="get_results",
)
async def get_results(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get all results for the current user."""

    with Session(db_engine) as session:
        results = (
            session.exec(select(Result).filter(Result.user_id == current_user.id))
            .unique()
            .all()
        )

    return results


@result_router.get(
    "/{result_id}",
    response_model=ResultRead,
    operation_id="get_result",
)
async def get_result(
    result_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get a result by ID for the current user."""

    with Session(db_engine) as session:
        result = session.get(Result, result_id)

    if result.user_id != current_user.id:
        return None

    return result


@result_router.put(
    "/{result_id}",
    response_model=ResultRead,
    operation_id="update_result",
)
async def update_result(
    result_id: int,
    result: ResultCreate,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update a result by ID for the current user."""

    with Session(db_engine) as session:
        db_result = session.get(Result, result_id)

        if db_result.user_id != current_user.id:
            return None

        db_result.quiz_id = result.quiz_id
        db_result.score = result.score
        db_result.total = result.total

        session.commit()
        session.refresh(db_result)

    return db_result


@result_router.delete(
    "/{result_id}",
    response_model=ResultRead,
    operation_id="delete_result",
)
async def delete_result(
    result_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete a result by ID for the current user."""

    with Session(db_engine) as session:
        result = session.get(Result, result_id)

        if result.user_id != current_user.id:
            return None

        session.delete(result)
        session.commit()

    return result
