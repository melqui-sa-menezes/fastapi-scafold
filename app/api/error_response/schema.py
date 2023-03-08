from datetime import datetime

from pydantic import BaseModel, Field


class MessageError(BaseModel):
    error_code: str
    error_message: str


class CreatedUpdatedSchema(BaseModel):
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Update date")


class NotFoundError(BaseModel):
    error_code: str = "not_found"
    error_message: str = "Product not found"
