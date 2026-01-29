from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class ProductsTable(Base):
    """Table containing products."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=True)
    sku = Column(String(255), nullable=True)

    unit = Column(String(255), nullable=False)

    net_price = Column(Numeric(10, 2), nullable=False)
    tax_rate = Column(Integer, nullable=False)
    gross_price = Column(Numeric(10, 2), nullable=False)

    is_active = Column(Boolean, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("CompaniesTable", back_populates="products")
