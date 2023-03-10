from fastapi.routing import APIRouter

from app.api import product, docs

api_router = APIRouter()

api_router.include_router(docs.router)

api_router.include_router(
    product.router,
    prefix="/product",
    tags=["product"],
)
