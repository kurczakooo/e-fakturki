from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.ksef_credentials import KsefCredentialsTable
from backend.web.api.ksef.schemas import KsefCertificatesUploadStatus

router = APIRouter()


@router.post(
    "/ksef/certificates", response_model=KsefCertificatesUploadStatus, status_code=201
)
async def upload_ksef_certificates(
    company_id: int = Form(...),
    certificates_for_auth: bool = Form(...),
    certificate: UploadFile = File(...),
    private_key: UploadFile = File(...),
    password: str = Form(...),
    db_session: AsyncSession = Depends(get_db_session),
) -> KsefCertificatesUploadStatus:
    """
    Uploads KSeF certificates for a company to the database.

    Args:
        company_id: The ID of the company.
        certificates_for_auth: Whether the uploaded certificates are for authentication (True) or for offline mode (False).
        certificate: The certificate file to be uploaded.
        private_key: The private key file to be uploaded.
        password: The password for the private key.
        db_session: The database session.

    Returns:
        An instance of KsefCertificatesUploadStatus containing the ID of the uploaded certificates.
    """

    # TODO encode the certs before saving to db, and decode when loading from db
    certificate_str = (await certificate.read()).decode("utf-8")
    private_key_str = (await private_key.read()).decode("utf-8")

    credentials = KsefCredentialsTable(
        company_id=company_id,
        encrypted_cert_auth=(certificate_str if certificates_for_auth else None),
        encrypted_private_key_auth=(private_key_str if certificates_for_auth else None),
        encrypted_password_auth=(password if certificates_for_auth else None),
        encrypted_cert_offline=(certificate_str if not certificates_for_auth else None),
        encrypted_private_key_offline=(
            private_key_str if not certificates_for_auth else None
        ),
        encrypted_password_offline=(password if not certificates_for_auth else None),
        encrypted_token=None,
        token_expires_at=None,
    )

    db_session.add(credentials)
    await db_session.flush()
    await db_session.refresh(credentials)
    return KsefCertificatesUploadStatus(ksef_certificates_id=int(credentials.id))
