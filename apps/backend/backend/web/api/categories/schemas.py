"""Schemas for Categories table."""

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """Schema for creating a new category record."""

    name: str
    description: str | None = None
    default_unit: str | None = None
    default_tax_rate: int | None = None


class CategoryRead(CategoryCreate):
    """Schema for reading a category record."""

    id: int

    class Config:
        from_attributes = True
