from sqlalchemy import select, func, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from backend.db.models.companies import CompaniesTable
from backend.web.api.companies.schemas import (
    CompaniesListItem,
    CompaniesListResponse,
    CompanyCreate,
    CompanyCreateResponse,
    CompanyUpdate,
    CompanyDetails,
)
from backend.web.api.invoices.schemas import PageInfo


async def get_company_nip(db: AsyncSession, company_id: int) -> str:
    """Get company NIP based on company ID."""
    stmt = select(CompaniesTable.nip).where(CompaniesTable.id == company_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_company_record(db: AsyncSession, company_id: str) -> str:
    """Delete a company record from the database."""
    stmt = select(CompaniesTable).where(CompaniesTable.id == company_id).limit(1)
    result = await db.execute(stmt)
    company = result.scalar_one()
    await db.delete(company)
    await db.commit()
    return company_id


async def get_company_by_user_id(
    db: AsyncSession, user_id: str
) -> CompaniesTable | None:
    """Get the company information associated with a given user ID."""
    stmt = select(CompaniesTable).where(CompaniesTable.owner_id == user_id).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_company_details_by_id(
    db: AsyncSession, company_id: int
) -> CompanyDetails:
    """Get company details based on company ID."""
    stmt = (
        select(
            CompaniesTable.id,
            CompaniesTable.krs,
            CompaniesTable.regon,
            CompaniesTable.address_correspondance_l1,
            CompaniesTable.address_correspondance_l2,
            CompaniesTable.additional_info,
        )
        .where(CompaniesTable.id == company_id)
        .limit(1)
    )
    result = await db.execute(stmt)
    company_details = result.mappings().one_or_none()
    return CompanyDetails(**company_details)


async def insert_new_company(
    db: AsyncSession, payload: CompanyCreate
) -> CompanyCreateResponse | None:
    """Insert a new company into the database."""
    try:
        company = CompaniesTable(**payload.model_dump())
        db.add(company)
        await db.commit()
        await db.refresh(company)

        return CompanyCreateResponse(user_id=company.owner_id, company_id=company.id)

    except IntegrityError:
        await db.rollback()
        raise


async def update_company_data(
    db: AsyncSession, payload: CompanyUpdate
) -> CompanyUpdate | None:
    """Update a company record in the database."""
    try:
        await db.execute(
            update(CompaniesTable)
            .where(CompaniesTable.id == payload.id)
            .values(
                name=payload.name,
                nip=payload.nip,
                krs=payload.krs,
                regon=payload.regon,
                email=payload.email,
                phone_number=payload.phone_number,
                country_code=payload.country_code,
                address_l1=payload.address_l1,
                address_l2=payload.address_l2,
                address_correspondance_l1=payload.address_correspondance_l1,
                address_correspondance_l2=payload.address_correspondance_l2,
                additional_info=payload.additional_info,
            )
        )

        await db.commit()
        return payload.id

    except IntegrityError:
        await db.rollback()
        raise


async def get_companies_list_paginated(
    db: AsyncSession, search_string: str | None, page_size: int, page_offset: int
) -> list[CompaniesListResponse]:
    """Get a paginated list of company records."""

    # Get total count of companies
    total_items = await db.execute(select(func.count(CompaniesTable.id)))
    total_items = total_items.scalar()

    # get the companies
    companies = await db.execute(
        select(
            CompaniesTable.id,
            CompaniesTable.owner_id,
            CompaniesTable.name,
            CompaniesTable.nip,
            CompaniesTable.country_code,
            CompaniesTable.address_l1,
            CompaniesTable.address_l2,
            CompaniesTable.email,
            CompaniesTable.phone_number,
        )
        .where(
            or_(
                CompaniesTable.name.contains(search_string),
                CompaniesTable.nip.contains(search_string),
                CompaniesTable.address_l1.contains(search_string),
                CompaniesTable.address_l2.contains(search_string),
                CompaniesTable.email.contains(search_string),
                CompaniesTable.phone_number.contains(search_string),
            )
        )
        .offset(page_offset)
        .limit(page_size)
        .order_by(CompaniesTable.name)
    )
    companies = [CompaniesListItem(**company) for company in companies.mappings().all()]

    # prepare page info
    page_info = PageInfo(
        current_page=(page_offset // page_size) + 1 if total_items > 0 else 1,
        page_size=page_size,
        total_items=total_items,
        has_next_page=(page_offset + page_size) < total_items,
        has_previous_page=page_offset > 0,
    )

    return CompaniesListResponse(companies=companies, page_info=page_info)
