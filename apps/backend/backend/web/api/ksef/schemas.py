"""Schemas for Ksef Communication."""

from pydantic import BaseModel


class KsefCertTypes(BaseModel):
    """Schema defining KSeF certificate types."""


class KsefInvoiceUpload(BaseModel):
    """Schema for uploading an invoice to KSeF."""

    company_id: int
    invoice_id: int


class KsefInvoiceUploadStatus(BaseModel):
    """Schema for reading invoice KSeF upload status."""

    company_id: int
    invoice_id: int

    ksef_status: str
    ksef_reference_number: str | None


class KsefCertificatesLoad(BaseModel):
    """Schema for storing KSeF certificates for a company. Encrypted or decrypted."""

    certificate: str
    private_key: str
    password: str


class KsefCertificatesUploadStatus(BaseModel):
    """Schema for status of uploading KSeF certificates to db."""

    ksef_certificates_id: int
