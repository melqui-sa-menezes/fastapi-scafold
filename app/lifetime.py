from typing import Awaitable, Callable

from fastapi import FastAPI

from app.db.dependencies import DBSession


def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.
    This function use fastAPI app to store data,
    such as db_engine.
    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    async def _startup() -> None:
        app.state.db_engine = DBSession().get_async_engine()

    return _startup


def shutdown(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.
    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    async def _shutdown() -> None:
        await app.state.db_engine.dispose()

    return _shutdown
