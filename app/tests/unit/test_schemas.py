from uuid import UUID

import pytest
from pydantic import ValidationError

from app.api.product.schemas import (
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
)


@pytest.mark.parametrize(
    "schema_cls, data, expected",
    [
        (
            ProductCreateSchema,
            {
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
            {
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
        ),
        (
            ProductCreateSchema,
            {"name": "", "description": "", "value": "invalid", "quantity": "invalid"},
            ValidationError,
        ),
        (
            ProductSchema,
            {
                "product_id": UUID("6d79a6c3-0f3b-4a5f-9c6f-2f2ff50b7df5"),
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
            {
                "product_id": UUID("6d79a6c3-0f3b-4a5f-9c6f-2f2ff50b7df5"),
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
        ),
        (
            ProductSchema,
            {
                "product_id": "invalid",
                "name": "",
                "description": "",
                "value": "invalid",
                "quantity": "invalid",
            },
            ValidationError,
        ),
        (
            ProductUpdateSchema,
            {
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
            {
                "name": "Product 1",
                "description": "This is a product",
                "value": 10.50,
                "quantity": 5,
            },
        ),
        (
            ProductUpdateSchema,
            {"name": "", "description": "", "value": "invalid", "quantity": "invalid"},
            ValidationError,
        ),
    ],
)
def test_schemas(schema_cls, data, expected):
    if expected == ValidationError:
        with pytest.raises(ValidationError):
            schema_cls(**data)
    else:
        schema = schema_cls(**data)
        assert schema.dict() == expected
