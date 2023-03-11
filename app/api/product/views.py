from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page

from app.api.error_response.schema import MessageError, NotFoundError
from app.api.helpers.query_parameters import product_query_parameters
from app.api.product.schemas import ProductCreateSchema, ProductUpdateSchema, \
    ProductSchema
from app.service.product_service import ProductService

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchema,
    responses={
        status.HTTP_409_CONFLICT: {"model": MessageError},
    },
)
async def create_product(
    payload: ProductCreateSchema,
    product_service: ProductService = Depends(ProductService),
):
    return await product_service.create_product(payload)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[ProductSchema],
)
async def get_all(
    product_service: ProductService = Depends(ProductService),
    product_id: Optional[UUID] = None,
    name: Optional[str] = None,
    description: Optional[str] = None
):
    query_filter = product_query_parameters(
        product_id=product_id,
        name=name,
        description=description
    )
    return await product_service.get_all_products(query_filter=query_filter)


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def get_by_product_id(
    product_id: UUID,
    product_service: ProductService = Depends(ProductService),
):
    return await product_service.get_by_product_id(product_id)


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_409_CONFLICT: {"model": MessageError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": MessageError},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def update_by_product_id(
    product_id: UUID,
    payload: ProductUpdateSchema,
    product_service: ProductService = Depends(ProductService),
):
    return await product_service.update_by_product_id(product_id, payload)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def delete_by_product_id(
    product_id: UUID,
    product_service: ProductService = Depends(ProductService),
):
    return await product_service.delete_by_product_id(product_id)
