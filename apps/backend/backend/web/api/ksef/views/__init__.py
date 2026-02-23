"""Views for KSEF API."""

from fastapi import APIRouter

from .post_ksef_certificates import router as post_ksef_certificates_router
from .post_single_invoice import router as post_single_invoice_router

router = APIRouter(prefix="/ksef", tags=["ksef"])

router.include_router(post_ksef_certificates_router)
router.include_router(post_single_invoice_router)
