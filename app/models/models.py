from sqlalchemy import DECIMAL, TEXT, Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Product(Base):
    __tablename__ = "product"
    __table_args__ = ()

    product_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String(256), nullable=False, unique=True)
    description = Column(TEXT, nullable=False)
    value = Column(DECIMAL(precision=10, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
