import random
from asyncio import current_task
from typing import AsyncGenerator, Callable

import factory
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, Headers
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.dependencies import db_session as dependency_db_session
from app.models.models import Product
from app.settings import settings


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    db_url_pg = str(settings.db_url).replace(
        f"{settings.db_url.port}{settings.db_url.path}",
        f"{settings.db_url.port}/postgres",
    )

    engine = create_async_engine(
        db_url_pg,
        echo=False,
    )
    session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)  # pylint: disable = no-member
        await connection.run_sync(
            Base.metadata.create_all,  # pylint: disable = no-member
        )
        async with session_factory(bind=connection) as session:
            yield session
    await engine.dispose()


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from app.application import get_app  # noqa: WPS433

    app = get_app()
    app.dependency_overrides[dependency_db_session] = override_get_db
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI, db_session: AsyncSession) -> AsyncGenerator:
    async def before_request(_):
        await db_session.commit()
        db_session.expire_all()

    async with AsyncClient(app=app, base_url="http://test", timeout=1) as ac:
        ac.event_hooks["request", "response"] = [before_request]
        yield ac


class AsyncFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    async def create(cls, **kwargs):
        result = super().create(**kwargs)
        await cls._meta.sqlalchemy_session.commit()  # pylint: disable=E1101
        await cls._meta.sqlalchemy_session.flush(result)  # pylint: disable=E1101
        return result

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


@pytest.fixture
def product_factory(db_session):
    class ProductFactory(AsyncFactory):
        class Meta:
            model = Product
            sqlalchemy_session = db_session

        product_id = factory.Faker("uuid4")
        name = factory.Faker("name")
        description = factory.Faker("text")
        value = factory.Faker("currency")
        quantity = random.randint(1, 999)

    return ProductFactory


@pytest_asyncio.fixture
async def product_mocked(product_factory):
    return await product_factory.create()
