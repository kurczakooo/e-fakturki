"""Database queries for companies table."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.companies import CompaniesTable


async def get_company_nip(db: AsyncSession, company_id: int) -> str:
    """Get company NIP based on company ID."""
    stmt = select(CompaniesTable.nip).where(CompaniesTable.id == company_id)
    result = await db.execute(stmt)
    return result.scalar_one()
