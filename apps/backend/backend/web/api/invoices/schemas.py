from pydantic import BaseModel
from datetime import datetime

from backend.db.models.invoices_brief import KsefStatus
from backend.db.repositories.invoices_payment_repository import InvoicePayment
from backend.db.repositories.invoices_entries_repository import InvoiceEntry


class PageInfo(BaseModel):
    """Pagination information for invoice list responses."""

    current_page: int
    page_size: int
    total_items: int
    has_next_page: bool
    has_previous_page: bool


class InvoicesListResponse(BaseModel):
    """Response model for invoice list with pagination info."""

    invoices: list[dict]
    page_info: PageInfo


class InvoiceCompanyData(BaseModel):
    """Response model for invoice buyer and seller detals."""

    name: str
    nip: str
    address_l1: str | None
    address_l2: str | None
    email: str | None
    phone: str | None


class InvoiceResponse(BaseModel):
    """Response model for full invoice with details."""

    id: str
    invoice_number: str
    invoice_type: str
    ksef_number: str | None
    invoicing_date: datetime | None
    acquisition_date: datetime | None
    permanent_storage_date: datetime | None
    ksef_status: KsefStatus
    is_new: bool
    ###
    issue_date: datetime
    issue_place: str | None
    ###
    seller_info: InvoiceCompanyData
    buyer_info: InvoiceCompanyData
    ###
    entries: list[InvoiceEntry]
    ###
    currency: str
    net_total: float
    tax_total: float
    gross_total: float
    ###
    payment: InvoicePayment | None
    ###
    annotations: str | None
    additional_info: str | None
    footer_info: str | None
    footer_registers: str | None
