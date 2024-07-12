"""Result router."""

from fastapi import APIRouter
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Result, ResultRead

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
