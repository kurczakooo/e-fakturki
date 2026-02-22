from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.db.base import Base


class InvoiceXmlSnapshotsTable(Base):
    """Table containing Invoices in XML format."""

    __tablename__ = "invoice_xml_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)

    xml = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    invoice = relationship("InvoicesTable", back_populates="invoice_xml_snapshots")
