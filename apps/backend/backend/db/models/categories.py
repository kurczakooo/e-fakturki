from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4

from backend.db.base import Base


class CategoriesTable(Base):
    """Table containing product categories."""

    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid4())
    )

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)

    default_unit: Mapped[str] = mapped_column(String(255), nullable=True)
    default_tax_rate: Mapped[str] = mapped_column(Integer, nullable=True)

    products = relationship("ProductsTable", back_populates="category")
    company = relationship("CompaniesTable", back_populates="categories")
