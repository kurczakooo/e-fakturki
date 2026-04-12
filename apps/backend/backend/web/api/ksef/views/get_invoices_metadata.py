from fastapi import APIRouter, Depends
from ksef_client import KsefClient, KsefClientOptions
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from backend.db.dependencies import get_db_session
from backend.db.repositories.company_repository import get_company_nip
from backend.services.ksef.auth.certificate_auth import (
    authorize_ksef_with_certificate,
    certificate_str_to_temp_file,
    remove_temp_file,
)
from backend.services.ksef.auth.ksef_session import open_ksef_session

from backend.web.api.ksef.schemas import SalesInvoicesRequest
from backend.web.api.ksef.services import get_auth_certs, to_iso
from backend.db.repositories.invoice_repository import insert_invoice

from backend.settings import Settings

router = APIRouter()


@router.post("/invoices", status_code=200, response_model=list[str])
async def get_invoices_list(
    payload: SalesInvoicesRequest,
    invoice_type: Literal["sales", "purchase"],
    db_session: AsyncSession = Depends(get_db_session),
) -> list[str]:
    """
    Download the invoices metadata list from KSeF and save them to the DB.

    https://api-demo.ksef.mf.gov.pl/docs/v2/index.html#tag/Pobieranie-faktur/paths/~1invoices~1query~1metadata/post
    """

    # load needed company data for the upload, including NIP and certs
    company_nip = await get_company_nip(db_session, payload.company_id)
    company_ksef_certs = await get_auth_certs(db_session, payload.company_id)
    password = company_ksef_certs.password
    cert_path = certificate_str_to_temp_file(company_ksef_certs.certificate)
    key_path = certificate_str_to_temp_file(company_ksef_certs.private_key)

    # paylaod creation
    request_payload = {
        "subjectType": "Subject1" if invoice_type == "sales" else "Subject2",
        "dateRange": {
            "dateType": "PermanentStorage",
            "from": to_iso(payload.date_from),
            "to": to_iso(payload.date_to),
        },
    }

    with KsefClient(KsefClientOptions(base_url=Settings.ksef_environment())) as client:
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

        metadata = client.invoices.query_invoice_metadata(
            request_payload,
            access_token=access_token,
            page_offset=payload.page_offset,
            page_size=payload.page_size,
            sort_order="Desc",
        )
        invoices = metadata.get("invoices") or metadata.get("invoiceList") or []

        ids = []
        for inv in invoices:
            inv_id = await insert_invoice(db_session, inv)
            ids.append(inv_id)

        ksef_session_params.workflow.close_session(
            ksef_session_params.session.session_reference_number, access_token
        )
        remove_temp_file(cert_path)
        remove_temp_file(key_path)

    return ids
