import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import configure_mappers, sessionmaker

from app.settings import settings

logging.basicConfig(level=logging.DEBUG)


class DBSession:
    async def __call__(self):
        async with self.db_session() as session:
            yield session

    @lru_cache
    def get_async_engine(self) -> AsyncEngine:
        url = str(settings.db_url)

        async_engine = create_async_engine(
            url,
            echo=settings.debug,
            pool_size=settings.db_pool_size,
            pool_recycle=settings.db_pool_recycle,
            max_overflow=settings.db_max_overflow,
        )

        configure_mappers()
        return async_engine

    @asynccontextmanager
    async def db_session(self) -> AsyncSession:
        session_factory = async_scoped_session(
            sessionmaker(
                self.get_async_engine(),
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )
        async_session = session_factory()

        try:
            yield async_session
            await async_session.commit()
        except Exception as err:
            logging.warning(f"Session rollback because of exception: {err}")
            await async_session.rollback()
            raise
        finally:
            await async_session.close()


db_session = DBSession()
