from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime

from backend.db.models.invoice_entries import InvoiceEntriesTable
from backend.db.mappings.invoices_entries_mappings import (
    map_fa3_fawiersz_to_invoice_entries_table,
)
import backend.domain.fa3_xml_utils.models.schemat as fa3utils


async def insert_invoice_entries(
    db: AsyncSession, fa3: fa3utils.Faktura, invoice_id: str
) -> list[str] | None:
    """Insert parsed invoice entries into InvoiceEntriesTable."""
    invoice_entries = []
    for entry in fa3.fa.fa_wiersz:
        invoice_entry = map_fa3_fawiersz_to_invoice_entries_table(entry, invoice_id)
        db.add(invoice_entry)
        await db.commit()
        await db.refresh(invoice_entry)
        invoice_entries.append(invoice_entry)

    return [entry.id for entry in invoice_entries]


class InvoiceEntry(BaseModel):
    """Response model for invoice list entry."""

    row_number: int
    delivery_date: str | datetime | None
    name: str
    amount: float
    unit: str
    net_price: float | None
    gross_price: float | None
    net_total: float | None
    tax_rate: int
    tax_total: float | None
    gross_total: float | None


async def get_invoice_entries_by_invoice_id(
    db: AsyncSession, invoice_id: str
) -> InvoiceEntry:
    """Get the invoice entries for the invoice with given ID."""
    stmt = select(
        InvoiceEntriesTable.row_number,
        InvoiceEntriesTable.delivery_date,
        InvoiceEntriesTable.name,
        InvoiceEntriesTable.amount,
        InvoiceEntriesTable.unit,
        InvoiceEntriesTable.net_price,
        InvoiceEntriesTable.gross_price,
        InvoiceEntriesTable.net_total,
        InvoiceEntriesTable.tax_rate,
        InvoiceEntriesTable.tax_total,
        InvoiceEntriesTable.gross_total,
    ).where(InvoiceEntriesTable.invoice_id == invoice_id)

    execution_result = await db.execute(stmt)
    result = execution_result.mappings().all()
    return [InvoiceEntry(**entry) for entry in result]
