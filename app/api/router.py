from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status

from app.api import docs, product
from app.api.error_response.schema import MessageError
from app.api.helpers.authenticator import authenticate_jwt

api_router = APIRouter()

api_router.include_router(docs.router)

api_router.include_router(
    product.router,
    prefix="/product",
    tags=["product"],
    dependencies=[Depends(authenticate_jwt)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": MessageError}
    }
)
