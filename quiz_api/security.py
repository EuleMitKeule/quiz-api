from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from starlette.status import HTTP_401_UNAUTHORIZED

from quiz_api.config import config
from quiz_api.const import API_PREFIX, CRYPT_ALGORITHM
from quiz_api.db import db_engine
from quiz_api.models import TokenData
from quiz_api.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/token")


def get_password_hash(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def get_user(username: str) -> User | None:
    with Session(db_engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        return user


def authenticate_user(username: str, password: str) -> User | bool:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, is_admin: bool, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    to_encode.update({"is_admin": is_admin})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=CRYPT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[CRYPT_ALGORITHM])
        username: str = payload.get("sub")
        is_admin: bool = payload.get("is_admin", False)

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, is_admin=is_admin)
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None or user.is_admin != token_data.is_admin:
        raise credentials_exception

    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> None:
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You must be an administrator to perform this action",
        )
