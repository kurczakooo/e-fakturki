import asyncio
from typing import Any

from ksef_client import KsefClient

from backend.services.ksef.auth.ksef_session import KsefSessionParams


def single_invoice_upload(
    ksef_session_params: KsefSessionParams,
    access_token: str,
    invoice_xml: bytes,
    offline_mode: bool | None = None,
    hash_of_corrected_invoice: str | None = None,
) -> Any:
    """
    Uploads XML of the invoice to KSEF API.

    Args:
        ksef_session_params: Parameters needed to run a ksef session.
        access_token: Access token for authentication.
        invoice_xml: XML string of the invoice to be uploaded.
        offline_mode: Whether to upload in offline mode.
        hash_of_corrected_invoice: Only if the invoice is a correction.

    Returns:
        An object containing the results of the upload, including the reference number.

    Todo:
        * handle errors statuses returned from the API.
    """
    return ksef_session_params.workflow.send_invoice(
        session_reference_number=ksef_session_params.session.session_reference_number,
        invoice_xml=invoice_xml,
        encryption_data=ksef_session_params.session.encryption_data,
        access_token=access_token,
        offline_mode=offline_mode,
        hash_of_corrected_invoice=hash_of_corrected_invoice,
    )


async def check_upload_status(
    client: KsefClient,
    ksef_session_params: KsefSessionParams,
    access_token: str,
    invoice_reference_number: str,
) -> Any:
    """
    Checks the status of the uploaded invoice in KSEF API.

    Runs in a loop until the status is no longer "processing",
    or "accepted for processing" or until timeout.

    Args:
        client: An instance of KsefClient.
        ksef_session_params: Parameters needed to run a ksef session.
        access_token: Access token for authentication.
        invoice_reference_number: Reference number of the uploaded invoice.

    Returns:
        An object containing the status of the uploaded invoice.
    """
    for _ in range(60):
        status = client.sessions.get_session_invoice_status(
            ksef_session_params.session.session_reference_number,
            invoice_reference_number,
            access_token=access_token,
        )

        code = int(status.get("status", {}).get("code", 0))

        if code == 200:
            return status
        if code not in {100, 150}:
            return status

        await asyncio.sleep(2)

    raise TimeoutError("Invoice upload status check timeout.")
