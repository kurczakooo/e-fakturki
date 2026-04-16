from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from backend.db.dependencies import get_db_session
from backend.db.repositories.company_repository import get_company_nip

from backend.web.api.ksef.schemas import SalesInvoicesRequest
from backend.web.api.invoices.schemas import InvoicesListResponse
from backend.db.repositories.invoice_repository import get_company_invoices_list

router = APIRouter()


@router.post("/invoices", status_code=200, response_model=InvoicesListResponse)
async def get_invoices_list(
    payload: SalesInvoicesRequest,
    invoice_type: Literal["sales", "purchase"],
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
