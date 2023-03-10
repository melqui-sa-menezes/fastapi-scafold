from typing import Optional

from pydantic import BaseModel, Field, UUID4, validator


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


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="")
    description: Optional[str] = Field(None, description="")
    value: Optional[float] = Field(None, description="")
    quantity: Optional[int] = Field(None, description="")
