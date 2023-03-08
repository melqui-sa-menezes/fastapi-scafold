from fastapi import Depends

from app.api.product.schemas import ProductCreateSchema
from app.models.models import Product
from app.repository.product_repository import ProductRepository


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository = Depends(),
    ):
        self.product_repository = product_repository

    async def create_product(self, payload: ProductCreateSchema):
        product_entity = Product(**payload.dict())
        return await self.product_repository.create(product_entity)
