from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from quiz_api.const import ACCESS_TOKEN_EXPIRE_MINUTES
from quiz_api.models import Token, User, UserRead
from quiz_api.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/token", operation_id="login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        is_admin=user.is_admin,
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me/", response_model=UserRead, operation_id="read_users_me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
