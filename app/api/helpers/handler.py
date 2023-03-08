import http

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from loguru import logger
from sqlalchemy.exc import NoResultFound
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.api.helpers.exception import (
    HTTPError,
    IntegrityException,
    RelatedIntegrityError,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NoResultFound)
    async def no_result_found(_: Request, exc: NoResultFound) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_404_NOT_FOUND,
                ).name.lower(),
                "error_message": str(exc),
            },
        )

    @app.exception_handler(HTTPError)
    async def http_error_handler(_: Request, exc: HTTPError) -> JSONResponse:
        headers = getattr(exc, "headers", None)
        return JSONResponse(
            {
                "error_code": exc.error_code,
                "error_message": exc.error_message,
            },
            status_code=exc.status_code,
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_422_UNPROCESSABLE_ENTITY,
                ).name.lower(),
                "error_message": jsonable_encoder(exc.errors()),
            },
        )

    @app.exception_handler(IntegrityException)
    async def request_integrity_error_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_409_CONFLICT,
                ).name.lower(),
                "error_message": str(exc),
            },
        )

    @app.exception_handler(RelatedIntegrityError)
    async def request_related_integrity_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_400_BAD_REQUEST,
                ).name.lower(),
                "error_message": str(exc),
            },
        )

    @app.exception_handler(Exception)
    async def request_error_internal_server_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.error(f"Internal server error [{_.url.path}] {str(exc)}")

        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_500_INTERNAL_SERVER_ERROR,
                ).name.lower(),
                "error_message": "",
            },
        )