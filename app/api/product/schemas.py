from typing import Optional

from pydantic import UUID4, BaseModel, Field, validator

from app.api.helpers.validators import (
    decimal_validator,
    empty_string_validator,
    number_validator,
)


class ProductCreateSchema(BaseModel):
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Brief description of the product")
    value: float = Field(..., description="Price of the product")
    quantity: int = Field(..., description="Quantity of product in stock")

    _empty_string_validator = validator("name", "description", allow_reuse=True)(
        empty_string_validator
    )
    _number_validator = validator("value", "quantity", allow_reuse=True)(
        number_validator
    )
    _value_validator = validator("value", allow_reuse=True)(decimal_validator)

    class Config:
        orm_mode = True


class ProductSchema(ProductCreateSchema):
    product_id: UUID4 = Field(..., description="")

    class Config:
        orm_mode = True


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="Product name")
    description: Optional[str] = Field(
        None, description="Brief description of the product"
    )
    value: Optional[float] = Field(None, description="Price of the product")
    quantity: Optional[int] = Field(None, description="Quantity of product in stock")

    _empty_string_validator = validator("name", "description", allow_reuse=True)(
        empty_string_validator
    )
    _number_validator = validator("value", "quantity", allow_reuse=True)(
        number_validator
    )
    _value_validator = validator("value", allow_reuse=True)(decimal_validator)
