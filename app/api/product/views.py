from fastapi import APIRouter, Depends, status

from app.api.error_response.schema import MessageError
from app.api.product.schemas import ProductCreateSchema
from app.service.product_service import ProductService

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": MessageError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageError},
    },
)
async def create_product(
    payload: ProductCreateSchema,
    product_service: ProductService = Depends(ProductService),
):
    return await product_service.create_product(payload)
