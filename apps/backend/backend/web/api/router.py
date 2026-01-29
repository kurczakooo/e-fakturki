from fastapi.routing import APIRouter

from backend.web.api import products

api_router = APIRouter()
api_router.include_router(products.router)
