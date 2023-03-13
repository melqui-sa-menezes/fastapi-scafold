from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.api.helpers.exception import HTTPError
from app.api.helpers.jwt_utils import decode_token

bearer_scheme = HTTPBearer()


async def authenticate_jwt(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = decode_token(token.credentials)
    except JWTError:
        raise HTTPError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_message="Invalid token"
        )
    return payload
