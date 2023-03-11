import sys
from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from loguru import logger

from starlette.middleware.cors import CORSMiddleware

from app.api.helpers.handler import register_exception_handlers
from app.api.router import api_router
from app.lifetime import shutdown, startup
from app.settings import settings

APP_ROOT = Path(__file__).parent
ROOT = Path(__file__).parent.parent

# Logger config
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level>  <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
    level="DEBUG",
    colorize=True,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.
    This is the main constructor of an application.
    :return: application.
    """

    app = FastAPI(
        title="app",
        description="Product API for MB Challenge",
        version=settings.api_version,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router)
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    register_exception_handlers(app)
    add_pagination(app)
    return app
