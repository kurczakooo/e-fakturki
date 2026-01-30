"""Category API views."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.categories import CategoriesTable
from backend.web.api.categories.schemas import CategoryCreate, CategoryRead

router = APIRouter()


@router.post("/categories", response_model=CategoryRead, status_code=201)
async def create_category(
    payload: CategoryCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> CategoryRead:
    """
    Create a new category record.

    :param payload: The data for creating a new category record.
    :param db_session: The database session.
    :return: The created category record.
    """

    category = CategoriesTable(
        name=payload.name,
        description=payload.description,
        default_unit=payload.default_unit,
        default_tax_rate=payload.default_tax_rate,
    )

    db_session.add(category)
    await db_session.flush()
    await db_session.refresh(category)
    return CategoryRead.model_validate(category)


@router.get("/categories", response_model=list[CategoryRead])
async def get_all_categories(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[CategoryRead]:
    """
    Get all category records.

    :param db_session: The database session.
    :return: A list of all category records.
    """
    statement = select(CategoriesTable)
    result = await db_session.execute(statement)
    categories = result.scalars().all()

    return [CategoryRead.model_validate(c) for c in categories]
