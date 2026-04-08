"""Ksef API services."""

from dateutil import parser

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.invoice_xml_snapshots import InvoiceXmlSnapshotsTable
from backend.db.models.ksef_credentials import KsefCredentialsTable
from backend.web.api.ksef.schemas import KsefCertificatesLoad


async def get_invoice_xml(db_session: AsyncSession, invoice_id: int) -> str:
    """
    Loads invoice xml from the database.

    Args:
        db_session: The database session.
        invoice_id: The ID of the invoice.

    Returns:
        The XML string of the invoice.
    """
    stmt = (
        select(InvoiceXmlSnapshotsTable.xml)
        .where(InvoiceXmlSnapshotsTable.id == invoice_id)
        .limit(1)
    )

    result = await db_session.execute(stmt)
    xml = result.scalar_one_or_none()

    if xml is None:
        raise ValueError(f"Invoice XML not found (invoice_id={invoice_id})")

    return xml


def xml_str_to_bytes(xml: str) -> bytes:
    """Turns str xml to bytes."""
    return xml.encode("utf-8")


def to_iso(date_str: str) -> str:
    """Converts a date string in various formats to ISO format (YYYY-MM-DD)."""
    try:
        dt = parser.parse(date_str, dayfirst=True)
        return dt.date().isoformat()
    except Exception as err:
        raise ValueError(f"Invalid date format: {date_str}") from err


async def get_auth_certs(
    db_session: AsyncSession, company_id: int
) -> KsefCertificatesLoad:
    """
    Loads cert, private_key and private_key_password from the database.

    Args:
        db_session: The database session.
        company_id: The ID of the company.

    Returns:
        An instance of KsefCertificatesLoad containing the cert, PK and password.

    """
    stmt = (
        select(
            KsefCredentialsTable.encrypted_cert_auth,
            KsefCredentialsTable.encrypted_private_key_auth,
            KsefCredentialsTable.encrypted_password_auth,
        )
        .where(KsefCredentialsTable.company_id == company_id)
        .limit(1)
    )

    result = await db_session.execute(stmt)
    row = result.first()

    if row is None:
        raise ValueError(f"Certificates not found for (company_id={company_id})")

    cert, key, password = row

    return KsefCertificatesLoad(
        certificate=cert,
        private_key=key,
        password=password,
    )
