"""Companies API views."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.addresses import AddressesTable
from backend.web.api.addresses.schemas import AddressCreate, AddressCreateResponse

router = APIRouter()


@router.post("/addresses", status_code=201, response_model=AddressCreateResponse)
async def create_address(
    payload: AddressCreate,
    db_session: AsyncSession = Depends(get_db_session),
) -> AddressCreateResponse:
    """Create a new address record linked to a company."""

    address = AddressesTable(
        company_id=payload.company_id,
        type=payload.type,
        country=payload.country,
        city=payload.city,
        postal_code=payload.postal_code,
        street=payload.street,
        building_number=payload.building_number,
    )

    db_session.add(address)
    await db_session.flush()
    await db_session.refresh(address)

    return AddressCreateResponse(company_id=address.company_id, address_id=address.id)
