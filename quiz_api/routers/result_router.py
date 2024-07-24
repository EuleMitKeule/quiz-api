"""Result router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Result, ResultRead
from quiz_api.security import require_admin

result_router = APIRouter(prefix="/result", tags=["result"])


@result_router.get(
    "",
    response_model=list[ResultRead],
    operation_id="get_results",
)
async def get_results(
    quiz_id: int | None = None,
    user_id: int | None = None,
):
    """Get all results for the current user."""

    query = select(Result)

    if quiz_id is not None:
        query = query.filter(Result.quiz_id == quiz_id)

    if user_id is not None:
        query = query.filter(Result.user_id == user_id)

    with Session(db_engine) as session:
        results = session.exec(query).unique().all()

    return results


@result_router.delete(
    "/{result_id}",
    response_model=int,
    operation_id="delete_result",
    dependencies=[Depends(require_admin)],
)
async def delete_result(result_id: int):
    """Delete a result by ID."""

    with Session(db_engine) as session:
        result = session.get(Result, result_id)

        if result is None:
            raise HTTPException(status_code=404, detail="Result not found.")

        session.delete(result)
        session.commit()

    return result_id
