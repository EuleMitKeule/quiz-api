"""Result router."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import Result, ResultCreate, ResultRead
from quiz_api.models import User
from quiz_api.security import get_current_user

result_router = APIRouter(prefix="/result", tags=["result"])


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
        results = session.exec(
            select(Result).filter(Result.user_id == current_user.id)
        ).all()

    return results


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
