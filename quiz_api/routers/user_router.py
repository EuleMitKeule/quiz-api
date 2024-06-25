from typing import Annotated

from fastapi import APIRouter, Depends

from quiz_api.models import User, UserRead
from quiz_api.security import get_current_user

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me", response_model=UserRead, operation_id="read_users_me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
