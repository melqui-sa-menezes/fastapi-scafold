from typing import Optional

from pydantic import BaseModel, Field, UUID4, validator

from app.api.helpers.validators import empty_string_validator, \
    decimal_validator, number_validator


class ProductCreateSchema(BaseModel):
    name: str = Field(..., description="")
    description: str = Field(..., description="")
    value: float = Field(..., description="")
    quantity: int = Field(..., description="")

    _empty_string_validator = validator("name", "description",
                                        allow_reuse=True)(
        empty_string_validator)
    _number_validator = validator("value", "quantity", allow_reuse=True)(
        number_validator)
    _value_validator = validator("value", allow_reuse=True)(decimal_validator)

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

    _empty_string_validator = validator("name", "description",
                                        allow_reuse=True)(
        empty_string_validator)
    _number_validator = validator("value", "quantity", allow_reuse=True)(
        number_validator)
    _value_validator = validator("value", allow_reuse=True)(decimal_validator)
