from enum import Enum as PyEnum
from typing import Never

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class AddressType(PyEnum):
    """Types of addresses."""

    reg = "registered"
    corr = "correspondence"


class AddressesTable(Base):
    """Table containing adresses."""

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    type: Column[Never] = Column(Enum(AddressType, name="address_type"), nullable=False)
    building_number = Column(String(10), nullable=False)
    street = Column(String(255), nullable=True)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)

    postal_code = Column(String(10), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("CompaniesTable", back_populates="addresses")
