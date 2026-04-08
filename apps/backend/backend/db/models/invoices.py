from enum import Enum as PyEnum
from typing import Never

from sqlalchemy import Column, DateTime, Enum, Numeric, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from backend.db.base import Base


class KsefStatus(PyEnum):
    """Statuses of an invoice in the ksef system."""

    not_sent = "not_sent"
    sent = "sent"
    acc = "accepted"
    rej = "rejected"


class PaymentStatus(PyEnum):
    """Statuses of an invoice."""

    unpaid = "unpaid"
    partial = "partial"
    paid = "paid"


class InvoicesTable(Base):
    """Table containing invoices."""

    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    invoice_number = Column(String(255), unique=True, nullable=False, index=True)

    issue_date = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    is_new = Column(Boolean, nullable=False, default=True, index=True)

    sale_place = Column(String(255), nullable=True)
    sale_date = Column(DateTime, nullable=True)

    seller_name = Column(String(255), nullable=False, index=True)
    seller_nip = Column(String(10), nullable=False, index=True)
    seller_address = Column(String(512), nullable=True)

    buyer_name = Column(String(255), nullable=False, index=True)
    buyer_nip = Column(String(10), nullable=False, index=True)
    buyer_address = Column(String(512), nullable=True)

    net_total = Column(Numeric(10, 2), nullable=False)
    tax_total = Column(Numeric(10, 2), nullable=False)
    gross_total = Column(Numeric(10, 2), nullable=False, index=False)
    currency = Column(String(255), nullable=False)

    payment_type = Column(String(255), nullable=True)
    payment_due_date = Column(DateTime, nullable=True)
    payment_status: Column[Never] = Column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.unpaid,
    )

    additional_info = Column(String(2048), nullable=True)

    ksef_number = Column(String(255), unique=True, nullable=True)
    ksef_status: Column[Never] = Column(
        Enum(KsefStatus, name="ksef_status"),
        nullable=False,
        default=KsefStatus.not_sent,
    )
    ksef_sent_at = Column(DateTime, nullable=True)

    invoice_xml_snapshots = relationship(
        "InvoiceXmlSnapshotsTable", back_populates="invoice"
    )
