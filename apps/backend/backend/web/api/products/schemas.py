"""Schemas for Product table."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    """Schema for creating a new product record."""

    company_id: int
    category_id: int | None = None

    name: str
    description: str | None = None
    sku: str | None = None

    unit: str | None = None

    net_price: Decimal
    tax_rate: int
    gross_price: Decimal | None = None


class ProductRead(ProductCreate):
    """Schema for reading a product record."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
