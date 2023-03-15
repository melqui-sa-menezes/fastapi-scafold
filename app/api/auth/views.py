from fastapi import APIRouter, status

from app.api.auth.schemas import TokenResponseSchema, CreateTokenSchema
from app.api.helpers.jwt_utils import create_token

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponseSchema,
)
async def get_token(payload: CreateTokenSchema):
    return create_token(payload.username)
