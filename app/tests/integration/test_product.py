from datetime import datetime
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from starlette import status

from app.models.models import Product
from app.tests.integration.stubs import CORRECT_PAYLOAD


@pytest.mark.asyncio
async def test_create_product_success(
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/product",
        json=CORRECT_PAYLOAD,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Produto Teste"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_update, msg_error",
    [
        ({"value": "string"}, "value is not a valid float"),
        ({"value": 0}, "The field must be greater than zero."),
        ({"value": 1.933}, "The value cannot have more than two decimal places"),
        ({"value": 10000000000.93}, "The value exceeds the expected size."),
        ({"name": ""}, "Field cannot be an empty string"),
        ({"description": "  "}, "Field cannot be an empty string"),
    ],
    ids=[
        "Deve falhar ao receber valor em string",
        "Deve falhar ao receber valor igual a zero",
        "Deve falhar ao receber valor com mais de duas casas decimais",
        "Deve falhar ao receber valor com inteiro maior que dez",
        "Deve falhar ao receber nome com string vazia",
        "Deve falhar ao receber description com string vazia",
    ],
)
async def test_create_product_fail_with_invalid_value_in_field(
    async_client: AsyncClient,
    data_update,
    msg_error
):
    payload = CORRECT_PAYLOAD
    payload.update(data_update)
    response = await async_client.post(
        "/product",
        json=payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["error_message"][0]["msg"] == msg_error


@pytest.mark.asyncio
async def test_create_product_fail_with_existing_name(
    async_client: AsyncClient,
    product_mocked,
):
    payload = {
        "name": product_mocked.name,
        "description": "Descrição qualquer do produto",
        "value": 529.89,
        "quantity": 73
    }
    response = await async_client.post(
        "/product",
        json=payload
    )
    print(f"updated_payload: {payload}")
    print(response.json())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["error_code"] == "conflict"
    assert response.json()["error_message"] == "Product integrity error"


@pytest.mark.asyncio
async def test_get_all_products_success_without_filter(
    async_client: AsyncClient,
    product_factory,
):
    await product_factory.create_batch(25)
    response = await async_client.get(
        "/product",
        params={"page": 1, "size": 10}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 25
    assert response.json()["size"] == 10


@pytest.mark.asyncio
async def test_get_all_products_success_with_filter_name(
    async_client: AsyncClient,
    product_factory,
):
    await product_factory.create(name="Camisa Adidas Running", description="Camisa feita para corrida")
    await product_factory.create(name="Bermuda Adidas Running", description="Bermuda feita para corrida")

    response = await async_client.get(
        "/product",
        params={"name": "Adidas", "page": 1, "size": 10}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 2


@pytest.mark.asyncio
async def test_get_all_products_success_with_filter_description_and_product_id(
    async_client: AsyncClient,
    product_factory,
):
    await product_factory.create(name="Camisa Adidas Running", description="Camisa feita para corrida")
    await product_factory.create(name="Bermuda Adidas Running", description="Bermuda feita para corrida")
    await product_factory.create(name="Tênis Nike Wiflo", description="Tênis feito para corrida")

    response = await async_client.get(
        "/product",
        params={"description": "Corrida", "page": 1, "size": 10}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 3

    product_id = response.json()["items"][0]["product_id"]
    response = await async_client.get(
        "/product",
        params={"product_id": product_id, "page": 1, "size": 10}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 1


@pytest.mark.asyncio
async def test_get_by_product_id_success(
    async_client: AsyncClient,
    product_mocked,
):
    response = await async_client.get(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == product_mocked.name


@pytest.mark.asyncio
async def test_get_by_product_id_with_product_deleted(
    async_client: AsyncClient,
    product_mocked,
):
    product_mocked.deleted_at = datetime.now()
    response = await async_client.get(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error_message"] == "Product not found"


@pytest.mark.asyncio
async def test_get_by_product_id_not_found(
    async_client: AsyncClient,
):
    response = await async_client.get(
        f"/product/{uuid4()}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error_message"] == "Product not found"


@pytest.mark.asyncio
async def test_get_by_product_id_invalid(
    async_client: AsyncClient,
):
    response = await async_client.get(
        "/product/72",
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["error_message"][0]["msg"] == "value is not a valid uuid"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_update, field, result",
    [
        ({"name": "Novo Nome"}, "name","Novo Nome"),
        ({"value": 23.75}, "value", 23.75),
        ({"quantity": 1}, "quantity", 1),
        ({"description": "Descrição atualizada"}, "description", "Descrição atualizada"),
    ],
    ids=[
        "Deve atualizar somente name",
        "Deve atualizar somente value",
        "Deve atualizar somente quantity",
        "Deve atualizar somente description",
    ],
)
async def test_update_by_product_id(
    async_client: AsyncClient,
    product_mocked,
    data_update,
    field,
    result
):
    response = await async_client.patch(
        f"/product/{product_mocked.product_id}",
        json=data_update,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[field] == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_update, msg_error",
    [
        ({"value": "string"}, "value is not a valid float"),
        ({"value": 0}, "The field must be greater than zero."),
        ({"value": 1.933}, "The value cannot have more than two decimal places"),
        ({"value": 10000000000.93}, "The value exceeds the expected size."),
        ({"name": ""}, "Field cannot be an empty string"),
        ({"description": "  "}, "Field cannot be an empty string"),
    ],
    ids=[
        "Deve falhar ao receber valor em string",
        "Deve falhar ao receber valor igual a zero",
        "Deve falhar ao receber valor com mais de duas casas decimais",
        "Deve falhar ao receber valor com inteiro maior que dez",
        "Deve falhar ao receber nome com string vazia",
        "Deve falhar ao receber description com string vazia",
    ],
)
async def test_update_product_fail_with_invalid_value_in_field(
    async_client: AsyncClient,
    product_mocked,
    data_update,
    msg_error
):
    payload = {
        "name": product_mocked.name,
        "description": "Descrição qualquer do produto",
        "value": 529.89,
        "quantity": 73
    }
    payload.update(data_update)
    response = await async_client.patch(
        f"/product/{product_mocked.product_id}",
        json=payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["error_message"][0]["msg"] == msg_error


@pytest.mark.asyncio
async def test_update_with_existing_name(
    async_client: AsyncClient,
    product_mocked,
    product_factory,
):
    other_product = await product_factory.create()
    payload = {"name": product_mocked.name}
    response = await async_client.patch(
        f"/product/{other_product.product_id}",
        json=payload,
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_delete_product_success(
    async_client: AsyncClient,
    db_session,
    product_mocked,
):
    response = await async_client.delete(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    statement = select(Product).filter_by(product_id=product_mocked.product_id)
    query_set = await db_session.execute(statement)
    product_db = query_set.scalar_one_or_none()
    assert product_db.deleted_at


@pytest.mark.asyncio
async def test_delete_product_success_deleted_at_unchanged(
    async_client: AsyncClient,
    db_session,
    product_mocked,
):
    response = await async_client.delete(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    statement = select(Product).filter_by(product_id=product_mocked.product_id)
    query_set = await db_session.execute(statement)
    first_product_db = query_set.scalar_one_or_none()
    assert first_product_db.deleted_at

    response = await async_client.delete(
        f"/product/{product_mocked.product_id}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    statement = select(Product).filter_by(product_id=product_mocked.product_id)
    query_set = await db_session.execute(statement)
    second_product_db = query_set.scalar_one_or_none()
    assert second_product_db.deleted_at == first_product_db.deleted_at


