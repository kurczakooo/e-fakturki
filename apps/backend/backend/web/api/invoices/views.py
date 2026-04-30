from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Literal

from backend.db.dependencies import get_db_session
from backend.db.repositories.company_repository import get_company_nip
from backend.db.models.invoices_payment import PaymentStatus
from backend.web.api.invoices.services import get_pretty_invoice_xml
from backend.web.api.auth.schemas import UserRead
from backend.web.api.auth.services import get_current_user
from backend.web.api.ksef.schemas import SalesInvoicesRequest
from backend.web.api.invoices.schemas import InvoicesListResponse
from backend.db.repositories.invoices_brief_repository import (
    get_company_invoices_list,
    update_invoice_payment_status,
    update_invoice_is_new_status,
)

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", status_code=200, response_model=InvoicesListResponse)
async def get_invoices_list(
    payload: SalesInvoicesRequest,
    invoice_type: Literal["sales", "purchase"],
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> InvoicesListResponse:
    """Download the invoices metadata list from DB."""
    company_nip = await get_company_nip(db_session, payload.company_id)

    return await get_company_invoices_list(
        db=db_session,
        filters=payload,
        company_nip=company_nip,
        invoice_type=invoice_type,
    )


@router.get("/{invoice_id}/pretty-xml", status_code=200, response_model=str)
async def get_invoice_xml(
    invoice_id: str = Path(..., description="The ID of the invoice."),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> str:
    """Get the formatted invoice XML from the database."""
    try:
        return await get_pretty_invoice_xml(db_session, invoice_id)
    except (IntegrityError, SQLAlchemyError) as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch("/{invoice_id}/payment-status", status_code=204)
async def update_payment_status(
    invoice_id: str = Path(..., description="The ID of the invoice to update."),
    new_payment_status: PaymentStatus = Query(
        ..., description="The new payment status to set for the invoice."
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> None:
    """Update the payment status of an invoice in the database."""

    try:
        success = await update_invoice_payment_status(
            db_session, invoice_id, new_payment_status
        )
        if not success:
            raise HTTPException(status_code=404, detail="Invoice not found")
    except (IntegrityError, SQLAlchemyError) as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.patch("/{invoice_id}/is-new", status_code=204)
async def update_new_status(
    invoice_id: str = Path(..., description="The ID of the invoice to update."),
    is_new: bool = Body(
        ..., description="Whether the invoice is new or not.", embed=True
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> None:
    """Update the is_new status of an invoice in the database."""

    try:
        success = await update_invoice_is_new_status(db_session, invoice_id, is_new)
        if not success:
            raise HTTPException(status_code=404, detail="Invoice not found")
    except (IntegrityError, SQLAlchemyError) as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
