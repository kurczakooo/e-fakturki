"""Schemas for Adresses table."""

from pydantic import BaseModel, Field

from backend.db.models.addresses import AddressType


class AddressCreate(BaseModel):
    """Schema for creating a new address record."""

    company_id: int = Field(
        ..., description="ID of the company this address belongs to"
    )
    type: AddressType = Field(..., description="Type of the address")
    country: str = Field(..., description="Country of the address")
    city: str = Field(..., description="City of the address")
    postal_code: str = Field(..., description="Postal code of the address")
    street: str = Field(..., description="Street of the address")
    building_number: str = Field(..., description="Building number of the address")


class AddressCreateResponse(BaseModel):
    """Return schema for creating a new address record."""

    company_id: int = Field(
        ..., description="ID of the company this address belongs to"
    )
    address_id: int = Field(..., description="ID of the created address record")
