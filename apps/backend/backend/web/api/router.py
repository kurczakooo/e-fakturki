from fastapi.routing import APIRouter

from backend.web.api import categories, products

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(categories.router)
