"""Database repository for users table."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.users import UsersTable


async def get_user_by_email(db: AsyncSession, email: str) -> UsersTable | None:
    """Fetch a user by email."""
    result = await db.execute(select(UsersTable).where(UsersTable.email == email))
    return result.scalars().first()
