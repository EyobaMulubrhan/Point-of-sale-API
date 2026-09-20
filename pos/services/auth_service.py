import jwt

from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from schemas.user import UserCreate
from repositories.user_repository import user_repository
from core.roles import Role


def register(db: Session, data: UserCreate):
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    values = data.model_dump(exclude={"password"})
    values["password_hash"] = hash_password(data.password)
    values["role"] = Role.CASHIER.value

    return user_repository.create(db, values)


def authenticate(
    db: Session,
    username: str,
    password: str,
):
    user = user_repository.get_by_username(db, username)

    if not user or not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return {
        "access_token": create_access_token(user.user_id),
        "token_type": "bearer",
    }


def get_user_from_token(db: Session, token: str):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = decode_access_token(token)

        subject = payload.get("sub")

        if not isinstance(subject, str) or not subject.strip():
            raise credentials_error

        user_id = UUID(subject)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_error

    user = user_repository.get_by_id(db, user_id)

    if user is None:
        raise credentials_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user