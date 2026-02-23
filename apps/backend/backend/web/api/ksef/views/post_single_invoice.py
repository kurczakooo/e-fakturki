from fastapi import APIRouter, Depends
from ksef_client import KsefClient, KsefClientOptions, KsefEnvironment
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.dao.companies_dao import get_company_nip
from backend.services.ksef.auth.certificate_auth import (
    authorize_ksef_with_certificate,
    certificate_str_to_temp_file,
    remove_temp_file,
)
from backend.services.ksef.auth.ksef_session import open_ksef_session
from backend.services.ksef.invoicing.upload import (
    check_upload_status,
    single_invoice_upload,
)
from backend.web.api.ksef.schemas import (
    KsefInvoiceUpload,
    KsefInvoiceUploadStatus,
)
from backend.web.api.ksef.services import (
    get_auth_certs,
    get_invoice_xml,
    xml_str_to_bytes,
)

router = APIRouter()


@router.post(
    "/ksef/single_upload", response_model=KsefInvoiceUploadStatus, status_code=202
)
async def upload_invoice_to_ksef(
    payload: KsefInvoiceUpload,
    db_session: AsyncSession = Depends(get_db_session),
    # TODO replace the base url to be taken from ENV or config file
    base_ksef_url: str = KsefEnvironment.DEMO.value,
) -> KsefInvoiceUploadStatus:
    """
    Upload single invoice to ksef.

    The invoice XML that needs to be uploaded should already be created,
    and stored in the database, this endpoint only handles the upload to KSeF,
    and checking the status of the upload.

    Args:
        payload: The data needed to upload the invoice (invoice ID and company ID).
        db_session: The database session.

    Returns:
        An instance of KsefInvoiceUploadStatus containing the status of the uploaded invoice.
    """
    # load the xml (needs to be in bytes)
    xml = await get_invoice_xml(db_session, payload.invoice_id)
    xml_bytes = xml_str_to_bytes(xml)
    # TODO validate the xml here

    # load needed company data for the upload, including NIP and certs
    company_nip = await get_company_nip(db_session, payload.company_id)
    company_ksef_certs = await get_auth_certs(db_session, payload.company_id)
    password = company_ksef_certs.password
    cert_path = certificate_str_to_temp_file(company_ksef_certs.certificate)
    key_path = certificate_str_to_temp_file(company_ksef_certs.private_key)

    with KsefClient(KsefClientOptions(base_url=base_ksef_url)) as client:
        certs = client.security.get_public_key_certificates()
        sym_cert = next(
            c["certificate"]
            for c in certs
            if "SymmetricKeyEncryption" in (c.get("usage") or [])
        )

        # authenticate with certs
        access_token = (
            authorize_ksef_with_certificate(
                certificate_path=cert_path,
                private_key_path=key_path,
                private_key_password=password,
                client=client,
                context_id_value=company_nip,
            )
        ).tokens.access_token.token

        ksef_session_params = open_ksef_session(
            client=client, access_token=access_token, sym_cert=sym_cert
        )

        sent_invoice_response = single_invoice_upload(
            ksef_session_params=ksef_session_params,
            access_token=access_token,
            invoice_xml=xml_bytes,
        )

        if sent_invoice_response.status() in [200, 201, 202]:
            upload_status = await check_upload_status(
                client=client,
                ksef_session_params=ksef_session_params,
                access_token=access_token,
                invoice_reference_number=sent_invoice_response["referenceNumber"],
            )

        ksef_session_params.workflow.close_session(
            ksef_session_params.session.session_reference_number, access_token
        )
        remove_temp_file(cert_path)
        remove_temp_file(key_path)

    return KsefInvoiceUploadStatus(
        company_id=payload.company_id,
        invoice_id=payload.invoice_id,
        ksef_status=upload_status["status"],
        ksef_reference_number=sent_invoice_response["referenceNumber"],
    )
