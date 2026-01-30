from sqlalchemy import Column, Integer, String

from backend.db.base import Base


class CategoriesTable(Base):
    """Table containing product categories."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=True)

    default_unit = Column(String(255), nullable=True)
    default_tax_rate = Column(Integer, nullable=True)
