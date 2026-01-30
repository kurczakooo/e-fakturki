from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class AccountsTable(Base):
    """Table containing bank accounts."""

    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    iban = Column(String(36), nullable=False)
    bank_name = Column(String(255), nullable=True)
    swift = Column(String(10), nullable=True)

    is_default = Column(Boolean, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("CompaniesTable", back_populates="bank_accounts")
