from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from backend.db.base import Base


class KsefCredentialsTable(Base):
    """Table containing KSeF credentials for a company (certificates, passwords, private keys, tokens)."""

    __tablename__ = "ksef_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("companies.id"), nullable=False
    )

    encrypted_cert_auth: Mapped[str] = mapped_column(Text, nullable=False)
    encrypted_private_key_auth: Mapped[str] = mapped_column(Text, nullable=False)
    encrypted_password_auth: Mapped[str] = mapped_column(Text, nullable=False)

    encrypted_cert_offline: Mapped[str] = mapped_column(Text, nullable=True)
    encrypted_private_key_offline: Mapped[str] = mapped_column(Text, nullable=True)
    encrypted_password_offline: Mapped[str] = mapped_column(Text, nullable=True)

    encrypted_token: Mapped[str] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    company = relationship("CompaniesTable", back_populates="ksef_credentials")
