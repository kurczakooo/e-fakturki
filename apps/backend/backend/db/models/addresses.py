import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from backend.db.base import Base


class AddressType(enum.StrEnum):
    """Types of addresses."""

    REGISTERED = "registered"
    CORRESPONDENCE = "correspondence"


class AddressesTable(Base):
    """Table containing adresses."""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    type: Mapped[str] = mapped_column(
        Enum(AddressType, name="address_type"), nullable=False
    )
    building_number: Mapped[str] = mapped_column(String(10), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)

    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    company = relationship("CompaniesTable", back_populates="addresses")
