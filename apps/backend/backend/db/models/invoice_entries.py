from sqlalchemy import Column, Float, ForeignKey, Integer, Numeric, String

from backend.db.base import Base


class InvoiceEntriesTable(Base):
    """Table containing invoice entries (sold products/services list)."""

    __tablename__ = "invoice_entries"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)

    order = Column(Integer, nullable=False)

    name = Column(String(255), nullable=False)
    amount = Column(Float(16), nullable=False)
    unit = Column(String(255), nullable=False)

    net_price = Column(Numeric(10, 2), nullable=False)
    net_total = Column(Numeric(10, 2), nullable=False)
    tax_rate = Column(Integer, nullable=False)
    tax_total = Column(Numeric(10, 2), nullable=False)
    gross_total = Column(Numeric(10, 2), nullable=False, index=True)
