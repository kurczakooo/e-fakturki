from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class KsefCredentialsTable(Base):
    """Table containing KSeF credentials for a company (certificates, passwords, private keys, tokens)."""

    __tablename__ = "ksef_credentials"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    encrypted_cert_auth = Column(Text, nullable=False)
    encrypted_private_key_auth = Column(Text, nullable=False)
    encrypted_password_auth = Column(Text, nullable=False)

    encrypted_cert_offline = Column(Text, nullable=True)
    encrypted_private_key_offline = Column(Text, nullable=True)
    encrypted_password_offline = Column(Text, nullable=True)

    encrypted_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("CompaniesTable", back_populates="ksef_credentials")
