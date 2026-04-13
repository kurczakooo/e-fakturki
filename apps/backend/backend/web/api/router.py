from fastapi.routing import APIRouter

from backend.web.api.auth import router as auth_router
from backend.web.api.products.views import router as products_router
from backend.web.api.categories.views import router as categories_router
from backend.web.api.companies.views import router as companies_router
from backend.web.api.addresses.views import router as addresses_router
from backend.web.api.invoices.views import router as invoices_router
from backend.web.api.ksef import router as ksef_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(products_router)
api_router.include_router(categories_router)
api_router.include_router(companies_router)
api_router.include_router(addresses_router)
api_router.include_router(invoices_router)
api_router.include_router(ksef_router)
