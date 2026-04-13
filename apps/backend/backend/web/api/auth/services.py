"""Auth API services."""

from pwdlib import PasswordHash
import jwt
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from datetime import datetime, timedelta, timezone

from backend.web.api.auth.schemas import UserRead
from backend.db.models.users import UsersTable
from fastapi import Depends, HTTPException, status
from backend.web.api.auth.schemas import TokenData
from backend.db.dependencies import get_db_session
from backend.settings import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    password_hasher = PasswordHash.recommended()
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with the given data and expiration."""
    to_encode = data.model_dump()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.algorithm)


async def get_current_user(
    token: Annotated[str, Depends(settings.oauth2_scheme)],
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRead:
    """Get the current user from the JWT token."""
    token: Annotated[str, Depends(settings.oauth2_scheme)]

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenData.model_validate(payload)

        if datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (InvalidTokenError, ValidationError):
        raise HTTPException from (InvalidTokenError, ValidationError)(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: UsersTable = await db_session.get(UsersTable, token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        last_name=user.last_name,
    )
