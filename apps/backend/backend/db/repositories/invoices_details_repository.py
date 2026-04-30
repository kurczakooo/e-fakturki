from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from pydantic import BaseModel

from backend.db.models.invoice_details import InvoiceDetailsTable
from backend.db.mappings.invoice_details_mappings import (
    map_fa3_to_invoice_details_table,
)
import backend.domain.fa3_xml_utils.models.schemat as fa3utils


async def insert_invoice_details(
    db: AsyncSession, fa3: fa3utils.Faktura, invoice_id: str
) -> str | None:
    """Insert parsed invoice details into InvoiceDetailsTable."""
    try:
        invoice_details_record = map_fa3_to_invoice_details_table(fa3, invoice_id)

        db.add(invoice_details_record)
        await db.commit()
        await db.refresh(invoice_details_record)

        return invoice_details_record.id

    except IntegrityError:
        await db.rollback()
        return None


class InvoiceDetailsResponse(BaseModel):
    """Response model for invoice detials."""

    issue_place: str | None
    seller_address_l1: str
    seller_address_l2: str | None
    seller_email: str | None
    seller_phone: str | None
    buyer_address_l1: str
    buyer_address_l2: str | None
    buyer_email: str | None
    buyer_phone: str | None
    annotation: str | None
    additional_info: str | None
    footer_info: str | None
    footer_registers: str | None


async def get_invoice_details_by_invoice_id(
    db: AsyncSession, invoice_id: str
) -> InvoiceDetailsResponse:
    """Get the invoice details for the invoice with given ID."""
    stmt = select(
        InvoiceDetailsTable.issue_place,
        InvoiceDetailsTable.seller_address_l1,
        InvoiceDetailsTable.seller_address_l2,
        InvoiceDetailsTable.seller_email,
        InvoiceDetailsTable.seller_phone,
        InvoiceDetailsTable.buyer_address_l1,
        InvoiceDetailsTable.buyer_address_l2,
        InvoiceDetailsTable.buyer_email,
        InvoiceDetailsTable.buyer_phone,
        InvoiceDetailsTable.annotation,
        InvoiceDetailsTable.additional_info,
        InvoiceDetailsTable.footer_info,
        InvoiceDetailsTable.footer_registers,
    ).where(InvoiceDetailsTable.invoice_id == invoice_id)

    execution_result = await db.execute(stmt)
    result = execution_result.mappings().one_or_none()
    return InvoiceDetailsResponse(**result) if result else None
