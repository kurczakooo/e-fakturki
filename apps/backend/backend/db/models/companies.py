from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class CompaniesTable(Base):
    """Table containing companies."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    nip = Column(String(10), nullable=False, unique=True)
    regon = Column(String(14), nullable=True, unique=True)
    krs = Column(String(10), nullable=True, unique=True)

    email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    additional_info = Column(String(2048), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("UsersTable", back_populates="companies")
