from fastapi.routing import APIRouter

from backend.web.api import categories, products
from backend.web.api.ksef import router as ksef_router

api_router = APIRouter()

api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(ksef_router)
