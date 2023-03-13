from datetime import datetime, timedelta
from jose import jwt

from app.settings import settings


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.algorithm)


def decode_token(token: str):
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.algorithm])
