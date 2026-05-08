from datetime import datetime

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """Schema for creating a new product record."""

    company_id: str = Field(..., description="ID of the company that owns the product")
    category_id: str | None = Field(None, description="Optional category ID")

    name: str = Field(..., description="Product name")
    description: str | None = Field(None, description="Product description")
    gtin: str | None = Field(
        None, description="Product GTIN (Global Trade Item Number)"
    )

    unit: str | None = Field(None, description="Unit of measurement (e.g. pcs, kg)")

    net_price: float = Field(..., description="Net price (without tax)")
    tax_rate: int = Field(..., description="Tax rate in percent (e.g. 23)")
    gross_price: float | None = Field(
        None,
        description="Gross price (with tax). If not provided, it will be calculated automatically",
    )


class ProductRead(BaseModel):
    """Schema for reading a product record."""

    id: int = Field(..., description="ID of the product record")
    created_at: datetime = Field(
        ..., description="Timestamp of when the product record was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp of when the product record was last updated"
    )

    class Config:
        from_attributes = True
