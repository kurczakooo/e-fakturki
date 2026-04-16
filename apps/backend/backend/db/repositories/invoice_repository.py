"""Database repository for invoices table."""

from datetime import datetime
from typing import Literal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from backend.web.api.ksef.schemas import SalesInvoicesRequest
from backend.db.models.invoices import InvoicesTable
from backend.web.api.invoices.schemas import InvoicesListResponse, PageInfo


def parse_date(value: str | None) -> datetime | None:
    """Convert ISO string to datetime, or return None if empty."""
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


async def insert_invoice(db: AsyncSession, invoice_data: dict) -> str:
    """Inserts a new invoice into the database."""
    try:
        invoice_record = InvoicesTable(
            invoice_number=invoice_data["invoiceNumber"],
            issue_date=parse_date(invoice_data["issueDate"]),
            is_new=True,
            sale_place=invoice_data.get("salePlace"),
            sale_date=parse_date(invoice_data["saleDate"])
            if "saleDate" in invoice_data
            else None,
            seller_name=invoice_data["seller"]["name"],
            seller_nip=invoice_data["seller"]["nip"],
            seller_address=invoice_data["seller"].get("address", None),
            buyer_name=invoice_data["buyer"]["name"],
            buyer_nip=invoice_data["buyer"]["identifier"]["value"]
            if invoice_data["buyer"]["identifier"]["type"] == "Nip"
            else "",
            buyer_address=invoice_data["buyer"].get("address", None),
            net_total=invoice_data["netAmount"],
            tax_total=invoice_data["vatAmount"],
            gross_total=invoice_data["grossAmount"],
            currency=invoice_data["currency"],
            payment_type=invoice_data["payment"]["type"]
            if "payment" in invoice_data
            else None,
            payment_due_date=parse_date(invoice_data["payment"]["dueDate"])
            if "payment" in invoice_data
            else None,
            payment_status="unpaid",
            ksef_number=invoice_data.get("ksefNumber"),
            ksef_status="acc" if invoice_data["ksefNumber"] is not None else "not_sent",
            ksef_sent_at=parse_date(invoice_data["acquisitionDate"])
            if invoice_data["acquisitionDate"] is not None
            else None,
        )

        db.add(invoice_record)
        await db.commit()
        await db.refresh(invoice_record)

        return invoice_record.id

    except IntegrityError:
        await db.rollback()
        return None


async def get_company_invoices_list(
    db: AsyncSession,
    filters: SalesInvoicesRequest,
    company_nip: str,
    invoice_type: Literal["sales", "purchase"],
) -> InvoicesListResponse:
    """Returns a list of invoices from the db, filtered and paginated."""

    # Decide on the filter condition
    if invoice_type == "sales":
        filter_condition = InvoicesTable.seller_nip == company_nip
    elif invoice_type == "purchase":
        filter_condition = InvoicesTable.buyer_nip == company_nip
    else:
        filter_condition = (InvoicesTable.seller_nip == company_nip) | (
            InvoicesTable.buyer_nip == company_nip
        )

    # Get total count of invoices
    total_items = await db.execute(
        select(func.count(InvoicesTable.id)).where(
            and_(
                filter_condition,
                InvoicesTable.issue_date >= parse_date(filters.date_from),
                InvoicesTable.issue_date <= parse_date(filters.date_to),
            )
        )
    )
    total_items = total_items.scalar()

    # Query db with filters and pagination
    result = await db.execute(
        select(
            InvoicesTable.id,
            InvoicesTable.invoice_number,
            InvoicesTable.issue_date,
            InvoicesTable.is_new,
            InvoicesTable.seller_name,
            InvoicesTable.buyer_name,
            InvoicesTable.gross_total,
            InvoicesTable.currency,
            InvoicesTable.payment_type,
            InvoicesTable.payment_status,
            InvoicesTable.ksef_number,
            InvoicesTable.ksef_status,
        )
        .where(
            and_(
                filter_condition,
                InvoicesTable.issue_date >= parse_date(filters.date_from),
                InvoicesTable.issue_date <= parse_date(filters.date_to),
            )
        )
        .order_by(InvoicesTable.issue_date.desc())
        .limit(filters.page_size)
        .offset(filters.page_offset)
    )
    data = [dict(row) for row in result.mappings().all()]

    page_info = PageInfo(
        current_page=(filters.page_offset // filters.page_size) + 1
        if total_items > 0
        else 1,
        page_size=filters.page_size,
        total_items=total_items,
        has_next_page=(filters.page_offset + filters.page_size) < total_items,
        has_previous_page=filters.page_offset > 0,
    )

    return InvoicesListResponse(invoices=data, page_info=page_info)
