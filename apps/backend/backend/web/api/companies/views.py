from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from backend.db.dependencies import get_db_session
from backend.db.repositories.company_repository import (
    get_company_by_user_id,
    insert_new_company,
    delete_company_record,
    update_company_data,
    get_companies_list_paginated,
    get_company_details_by_id,
)
from backend.domain.fa3_xml_utils.models.kody_krajow_v10_0_e import TkodKraju
from backend.web.api.companies.services import get_polish_country_name
from backend.db.repositories.ksef_credentials_repository import get_ksef_credentials
from backend.web.api.auth.schemas import UserRead
from backend.web.api.auth.services import get_current_user
from backend.web.api.companies.schemas import (
    CompanyCreate,
    CompanyCreateResponse,
    CompanyDetails,
    CompanyUpdate,
    IsoCountry,
    UserCompanyResponse,
    CompaniesListResponse,
)

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("", status_code=201, response_model=CompanyCreateResponse)
async def create_company(
    payload: CompanyCreate,
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> CompanyCreateResponse:
    """Create a new company record."""
    try:
        company_response = await insert_new_company(db_session, payload)
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Firma z tym numerem NIP już istnieje w bazie danych",
        ) from e

    return company_response


@router.delete("/{company_id}", status_code=204)
async def delete_company(
    company_id: str = Path(
        ..., description="The ID of the company to delete from the db."
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a company record."""
    try:
        await delete_company_record(db_session, company_id)
    except NoResultFound as e:
        raise HTTPException(
            status_code=422,
            detail="W bazie danych nie ma firmy z podanym ID",
        ) from e


@router.put("", status_code=201, response_model=CompanyUpdate)
async def update_company(
    payload: CompanyUpdate,
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> CompanyUpdate:
    """Update a company record."""
    try:
        company_update_response = await update_company_data(db_session, payload)
    except IntegrityError as e:
        raise HTTPException(
            status_code=422,
            detail="Firma z tym numerem NIP już istnieje w bazie danych",
        ) from e

    return company_update_response


@router.get("/user", status_code=200, response_model=UserCompanyResponse)
async def get_user_company(
    user_id: str = Query(
        ...,
        description="The ID of the user whose company information is being requested.",
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserCompanyResponse:
    """Fetch the company information associated with the current user."""

    company = await get_company_by_user_id(db_session, user_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found for the user.")

    # check if company has KSeF credentials in the DB
    ksef_creds = await get_ksef_credentials(db_session, company.id)
    if not (
        ksef_creds.encrypted_cert_auth
        and ksef_creds.encrypted_private_key_auth
        and ksef_creds.encrypted_password_auth
    ):
        raise HTTPException(
            status_code=409, detail="KSeF credentials not found for the company."
        )

    return UserCompanyResponse(
        company_id=company.id,
        name=company.name,
        nip=company.nip,
        country_code=company.country_code,
        address_l1=company.address_l1,
        address_l2=company.address_l2,
        email=company.email,
        phone_number=company.phone_number,
        ksef_authorized=True,
    )


@router.get("", status_code=200, response_model=CompaniesListResponse)
async def get_companies_list(
    search_string: str = Query(
        None, description="The search string to filter the company list."
    ),
    page_size: int = Query(
        10,
        description="The number of company records to retrieve per page. [10 ... 250]",
    ),
    page_offset: int = Query(
        0,
        description="The offset for pagination, i.e. the number of records to skip before starting to collect the result set.",
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> CompaniesListResponse:
    """Get all company records."""

    try:
        return await get_companies_list_paginated(
            db_session, search_string, page_size, page_offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/details", status_code=200, response_model=CompanyDetails)
async def get_company_details(
    company_id: str = Query(
        ...,
        description="The ID of the company whose details are being requested.",
    ),
    current_user: UserRead = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> CompanyDetails:
    """Fetch the company details."""

    try:
        company = await get_company_details_by_id(db_session, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found.")
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Company not found.") from e

    return company


@router.get("/iso-countries", status_code=200, response_model=list[IsoCountry])
async def get_iso_countries(
    current_user: UserRead = Depends(get_current_user),
) -> list[IsoCountry]:
    """Get all ISO countries list."""

    return [get_polish_country_name(iso_country.value) for iso_country in TkodKraju]
