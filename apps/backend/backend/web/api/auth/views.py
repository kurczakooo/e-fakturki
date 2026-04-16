"""Auth API views."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pwdlib import PasswordHash
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.db.models.users import UsersTable
from backend.web.api.auth.schemas import UserCreate, UserRead, TokenData, Token
from backend.web.api.auth.services import (
    verify_password,
    create_access_token,
    get_current_user,
)
from backend.db.dependencies import get_db_session
from backend.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201, response_model=Token)
async def signup_user(
    payload: UserCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    """Create and authorize a new user."""

    result = await db_session.execute(
        select(UsersTable).where(UsersTable.email == payload.email)
    )
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=401,
            detail="User with this email already exist",
        )

    password_hasher = PasswordHash.recommended()

    user = UsersTable(
        name=payload.name,
        last_name=payload.last_name,
        email=payload.email,
        password=password_hasher.hash(payload.password),
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    claims = TokenData(
        sub=user.id, email=user.email, name=user.name, last_name=user.last_name
    )

    return Token(
        access_token=create_access_token(claims), token_type=settings.token_type
    )


@router.post("/login", status_code=200)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    """Authorize a user and return an access token."""

    result = await db_session.execute(
        select(UsersTable).where(UsersTable.email == form_data.username)
    )
    user = result.scalars().first()

    if not user or not verify_password(
        plain_password=form_data.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    claims = TokenData(
        sub=user.id, email=user.email, name=user.name, last_name=user.last_name
    )

    return Token(
        access_token=create_access_token(claims), token_type=settings.token_type
    )


@router.get("/me", status_code=200, response_model=UserRead)
async def get_me(
    current_user: UserRead = Depends(get_current_user),
) -> UserRead:
    """Get the current authorized user."""
    return current_user
