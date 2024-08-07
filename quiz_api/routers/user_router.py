from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from quiz_api.db import db_engine
from quiz_api.models import User, UserCreate, UserRead
from quiz_api.security import get_current_user, get_password_hash, require_admin

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post(
    "",
    response_model=UserRead,
    operation_id="create_user",
    dependencies=[Depends(require_admin)],
)
async def create_user(user_create: UserCreate):
    """Create a user."""

    user = User(
        username=user_create.username,
        hashed_password=get_password_hash(user_create.password),
        is_admin=user_create.is_admin,
    )

    with Session(db_engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


@user_router.get("/me", response_model=UserRead, operation_id="read_users_me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@user_router.get(
    "",
    response_model=list[UserRead],
    operation_id="read_users",
)
async def read_users():
    with Session(db_engine) as session:
        users = session.exec(select(User)).unique().all()

        return users


@user_router.get(
    "/{user_id}",
    response_model=UserRead,
    operation_id="read_user",
    dependencies=[Depends(require_admin)],
)
async def read_user(user_id: int):
    with Session(db_engine) as session:
        user = session.get(User, user_id)

        return user


@user_router.put(
    "/{user_id}",
    response_model=UserRead,
    operation_id="update_user",
)
async def update_user(
    user_id: int,
    user_create: UserCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this user.",
        )

    with Session(db_engine) as session:
        user = session.get(User, user_id)
        user.is_admin = user_create.is_admin

        if user_create.password:
            user.hashed_password = get_password_hash(user_create.password)

        session.commit()
        session.refresh(user)

    return user


@user_router.delete(
    "/{user_id}",
    response_model=int,
    operation_id="delete_user",
    dependencies=[Depends(require_admin)],
)
async def delete_user(user_id: int):
    with Session(db_engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()

    return user_id
