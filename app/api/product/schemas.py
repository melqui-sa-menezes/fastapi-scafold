from pydantic import BaseModel, Field, UUID4


class ProductCreateSchema(BaseModel):
    name: str = Field(..., description="")
    description: str = Field(..., description="")
    value: float = Field(..., description="")
    quantity: int = Field(..., description="")

    class Config:
        orm_mode = True


class ProductSchema(ProductCreateSchema):
    product_id: UUID4 = Field(..., description="")

    class Config:
        orm_mode = True
