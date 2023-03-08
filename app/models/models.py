from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    DECIMAL,
    Integer,
    String,
    text
)

from app.db.base import Base


class Product(Base):
    __tablename__ = "product"
    __table_args__ = ()

    product_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    value = Column(DECIMAL(precision=10, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
