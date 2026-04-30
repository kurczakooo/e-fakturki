from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.ksef_credentials import KsefCredentialsTable


class KsefCertificatesLoad(BaseModel):
    """Schema for storing KSeF certificates for a company. Encrypted or decrypted."""

    certificate: str
    private_key: str
    password: str


async def get_ksef_credentials(
    db: AsyncSession, company_id: int
) -> KsefCredentialsTable | None:
    """Get the KSeF credentials for the company with given ID."""
    stmt = select(KsefCredentialsTable).where(
        KsefCredentialsTable.company_id == company_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_auth_certs(
    db_session: AsyncSession, company_id: int
) -> KsefCertificatesLoad:
    """Loads cert, private_key and private_key_password from the database."""
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
