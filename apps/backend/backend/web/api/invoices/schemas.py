"""Schemas for invoices API."""

from pydantic import BaseModel


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
