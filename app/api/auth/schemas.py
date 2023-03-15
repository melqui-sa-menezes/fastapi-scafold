from pydantic import BaseModel, Field


class CreateTokenSchema(BaseModel):
    username: str = Field(
        "username",
        description="Username for generate JWT token"
    )


class TokenResponseSchema(BaseModel):
    access_token: str = Field(..., description="Valid JWT token")
