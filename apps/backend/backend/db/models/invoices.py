from enum import Enum as PyEnum
from typing import Never

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.sql import func

from backend.db.base import Base


class StatusType(PyEnum):
    """Statuses of an invoice."""

    df = "draft"
    iss = "issued"
    paid = "paid"


class KsefStatus(PyEnum):
    """Statuses of an invoice in the ksef system."""

    not_sent = "not_sent"
    sent = "sent"
    acc = "accepted"
    rej = "rejected"


class InvoicesTable(Base):
    """Table containing invoices."""

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(255), unique=True, nullable=False, index=True)

    issue_date = Column(DateTime, server_default=func.now(), nullable=False)

    sale_place = Column(String(255), nullable=False)
    sale_date = Column(DateTime, server_default=func.now(), nullable=False)

    seller_name = Column(String(255), nullable=False, index=True)
    seller_nip = Column(String(10), nullable=False, index=True)
    seller_address = Column(String(512), nullable=False)

    buyer_name = Column(String(255), nullable=False, index=True)
    buyer_nip = Column(String(10), nullable=False, index=True)
    buyer_address = Column(String(512), nullable=False)

    net_total = Column(Numeric(10, 2), nullable=False)
    tax_total = Column(Numeric(10, 2), nullable=False)
    gross_total = Column(Numeric(10, 2), nullable=False, index=True)
    currency = Column(String(255), nullable=False)

    payment_type = Column(String(255), nullable=False)
    payment_due_date = Column(DateTime, nullable=False)

    additional_info = Column(String(2048), nullable=True)
    status: Column[Never] = Column(
        Enum(StatusType, name="status_type"), nullable=False, default=StatusType.df
    )

    ksef_id = Column(String(255), unique=True, nullable=True)
    ksef_status: Column[Never] = Column(
        Enum(KsefStatus, name="ksef_status"),
        nullable=False,
        default=KsefStatus.not_sent,
    )
    ksef_sent_at = Column(DateTime, nullable=True)
