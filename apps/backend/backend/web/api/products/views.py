"""Product API views."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.products import ProductsTable
from backend.web.api.products.schemas import ProductCreate, ProductRead
from backend.web.api.products.services import check_and_set_gross_price

router = APIRouter()


@router.post("/products", response_model=ProductRead, status_code=201)
async def create_dummy(
    payload: ProductCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> ProductRead:
    """
    Create a new product record.

    :param payload: The data for creating a new product record.
    :param db_session: The database session.
    :return: The created product record.
    """
    payload = check_and_set_gross_price(payload)

    product = ProductsTable(
        name=payload.name,
        description=payload.description,
        sku=payload.sku,
        category_id=payload.category_id,
        net_price=payload.net_price,
        tax_rate=payload.tax_rate,
        gross_price=payload.gross_price,
    )

    db_session.add(product)
    await db_session.flush()
    await db_session.refresh(product)
    return ProductRead.model_validate(product)


@router.get("/products", response_model=list[ProductRead])
async def get_all_dummy(
    db_session: AsyncSession = Depends(get_db_session),
) -> list[ProductRead]:
    """
    Get all product records.

    :param db_session: The database session.
    :return: A list of all products records.
    """
    statement = select(ProductsTable)
    result = await db_session.execute(statement)
    products = result.scalars().all()

    return [ProductRead.model_validate(p) for p in products]
