from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import db_session
from app.models.models import Product
from app.repository.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(db_session)): # pragma: no cover
        super().__init__(session, Product)
