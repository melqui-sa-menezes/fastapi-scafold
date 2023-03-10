from fastapi import Depends

from app.api.product.schemas import ProductCreateSchema, ProductUpdateSchema
from app.models.models import Product
from app.repository.product_repository import ProductRepository


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository = Depends(),
    ):
        self.product_repository = product_repository

    async def create_product(self, payload: ProductCreateSchema):
        return await self.product_repository.create(Product(**payload.dict()))

    async def get_all_products(self):
        return await self.product_repository.get_all()

    async def get_by_id(self, product_id):
        return await self.product_repository.get_by_id(product_id)

    async def update_by_product_id(self, product_id, data: dict):
        return await self.product_repository.update_by_id(product_id, data)
