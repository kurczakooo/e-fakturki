from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel

from backend.db.models.invoices_payment import (
    InvoicesPaymentTable,
    PaymentStatus,
    PaymentType,
)
from backend.db.mappings.invoice_payment_mappings import (
    map_fa3_fa_platnosc_to_invoices_payment_table,
)
import backend.domain.fa3_xml_utils.models.schemat as fa3utils


async def insert_invoice_payment_details(
    db: AsyncSession, fa3: fa3utils.Faktura, invoice_id: str
) -> str | None:
    """Insert parsed invoice payment details into InvoicesPaymentTable."""
    try:
        if fa3.fa.platnosc is None:
            return None

        invoice_payment_record = map_fa3_fa_platnosc_to_invoices_payment_table(
            fa3.fa.platnosc, invoice_id
        )

        db.add(invoice_payment_record)
        await db.commit()
        await db.refresh(invoice_payment_record)

        return invoice_payment_record.id

    except IntegrityError:
        await db.rollback()
        return None


class InvoicePayment(BaseModel):
    """Response model for invoice payment."""

    payment_status: PaymentStatus
    payment_type: PaymentType
    payment_date: str | datetime | None
    payment_due_date: str | datetime | None
    partial_payments: str | None
    seller_bank_account_number: str | None
    seller_bank_name: str | None


async def get_invoice_payment_by_invoice_id(
    db: AsyncSession, invoice_id: str
) -> InvoicePayment:
    """Get the invoice payment info for the invoice with given ID."""
    stmt = select(
        InvoicesPaymentTable.payment_status,
        InvoicesPaymentTable.payment_type,
        InvoicesPaymentTable.payment_date,
        InvoicesPaymentTable.payment_due_date,
        InvoicesPaymentTable.partial_payments,
        InvoicesPaymentTable.seller_bank_account_number,
        InvoicesPaymentTable.seller_bank_name,
    ).where(InvoicesPaymentTable.invoice_id == invoice_id)

    execution_result = await db.execute(stmt)
    result = execution_result.mappings().one_or_none()
    return InvoicePayment(**result) if result else None
