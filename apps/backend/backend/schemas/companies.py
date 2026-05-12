from pydantic import BaseModel, Field

from backend.schemas.invoices import PageInfo


class CompanyCreate(BaseModel):
    """Schema for creating a new company record."""

    owner_id: str | None = Field(
        None, description="The ID of the user who owns the company."
    )
    name: str = Field(..., description="The name of the company.")
    nip: str = Field(
        ..., description="The NIP (tax identification number) of the company."
    )
    krs: str | None = Field(
        None,
        description="The KRS (National Court Register) number of the company, if applicable.",
    )
    regon: str | None = Field(
        None,
        description="The REGON (statistical number) of the company, if applicable.",
    )
    country_code: str = Field(..., description="Country the company is registered in.")
    address_l1: str | None = Field(None, description="First line of company's address.")
    address_l2: str | None = Field(
        None, description="Second line of company's address."
    )
    address_correspondance_l1: str | None = Field(
        None, description="First line of company's correspondance address."
    )
    address_correspondance_l2: str | None = Field(
        None, description="Second line of company's correspondance address."
    )
    email: str | None = Field(None, description="Company's email address.")
    phone_number: str | None = Field(None, description="Company's phone number.")
    additional_info: str | None = Field(
        None, description="Any additional info about the company."
    )


class CompanyCreateResponse(BaseModel):
    """Return schema for creating a new company record."""

    user_id: str | None = Field(
        None, description="The ID of the user who owns the company."
    )
    company_id: str = Field(
        ..., description="The ID of the created company record in the database."
    )


class CompanyUpdate(BaseModel):
    """Return schema for updating a company record."""

    id: str = Field(
        ..., description="The ID of the updated company record in the database."
    )
    name: str = Field(..., description="The name of the company.")
    nip: str = Field(
        ..., description="The NIP (tax identification number) of the company."
    )
    krs: str | None = Field(
        None,
        description="The KRS (National Court Register) number of the company, if applicable.",
    )
    regon: str | None = Field(
        None,
        description="The REGON (statistical number) of the company, if applicable.",
    )
    country_code: str = Field(..., description="Country the company is registered in.")
    address_l1: str | None = Field(None, description="First line of company's address.")
    address_l2: str | None = Field(
        None, description="Second line of company's address."
    )
    address_correspondance_l1: str | None = Field(
        None, description="First line of company's correspondance address."
    )
    address_correspondance_l2: str | None = Field(
        None, description="Second line of company's correspondance address."
    )
    email: str | None = Field(None, description="Company's email address.")
    phone_number: str | None = Field(None, description="Company's phone number.")
    additional_info: str | None = Field(
        None, description="Any additional info about the company."
    )


class UserCompanyResponse(BaseModel):
    """Return schema for fetching a user's company information."""

    company_id: str = Field(
        ..., description="The ID of the company record in the database."
    )
    name: str = Field(..., description="The name of the company.")
    nip: str = Field(
        ..., description="The NIP (tax identification number) of the company."
    )
    country_code: str | None = Field(
        None, description="Country the company is registered in."
    )
    address_l1: str | None = Field(None, description="First line of company's address.")
    address_l2: str | None = Field(
        None, description="Second line of company's address."
    )
    email: str | None = Field(None, description="Company's email address.")
    phone_number: str | None = Field(None, description="Company's phone number.")
    ksef_authorized: bool = Field(
        ..., description="Indicates whether the company is authorized to use KSeF."
    )


class CompaniesListItem(BaseModel):
    """Schema for companies list item."""

    id: str = Field(..., description="The ID of the company record in the database.")
    owner_id: str | None = Field(
        None, description="The ID of the user who owns the company."
    )
    name: str = Field(..., description="The name of the company.")
    nip: str = Field(
        ..., description="The NIP (tax identification number) of the company."
    )
    country_code: str | None = Field(
        None, description="Country the company is registered in."
    )
    address_l1: str | None = Field(None, description="First line of company's address.")
    address_l2: str | None = Field(
        None, description="Second line of company's address."
    )
    email: str | None = Field(None, description="Company's email address.")
    phone_number: str | None = Field(None, description="Company's phone number.")


class CompanyDetails(BaseModel):
    """Return schema for company details."""

    id: str = Field(..., description="The ID of the company record in the database.")
    krs: str | None = Field(
        None,
        description="The KRS (National Court Register) number of the company, if applicable.",
    )
    regon: str | None = Field(
        None,
        description="The REGON (statistical number) of the company, if applicable.",
    )
    address_correspondance_l1: str | None = Field(
        None, description="First line of company's correspondance address."
    )
    address_correspondance_l2: str | None = Field(
        None, description="Second line of company's correspondance address."
    )
    additional_info: str | None = Field(
        None, description="Any additional info about the company."
    )


class CompaniesListResponse(BaseModel):
    """Return schema for companies list."""

    companies: list[CompaniesListItem]
    page_info: PageInfo


class IsoCountry(BaseModel):
    """Return schema for ISO countries list."""

    name: str
    code: str
