import logging

from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import and_, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncScalarResult, AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from app.api.helpers.exception import IntegrityException
from app.db.base import Base


class BaseRepository:
    """Class for accessing model table."""

    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    async def create(self, base_model: Base) -> Base:
        """Add single model to database.
        :param base_model: model.
        :return: a model.
        """
        try:
            self.session.add(base_model)
            await self.session.flush()
            await self.session.refresh(base_model)
            return base_model
        except IntegrityError:
            await self.session.rollback()
            raise IntegrityException(f"{self.model.__name__} integrity error")

    async def bulk_insert_objects(self, objects: list) -> None:
        """Add many rows of a model to database."""
        try:
            self.session.add_all(objects)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise IntegrityException(f"{self.model.__name__} integrity error")

    async def bulk_update(self, models_ids: list, data_to_update: dict):
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")

        blocks_updated = await self.session.execute(
            update(self.model).filter(model_id.in_(models_ids)).values(data_to_update),
        )
        return blocks_updated  # noqa: WPS331

    async def get_all(
        self,
        query_filter=None,
    ) -> AsyncScalarResult:
        """Get all models.
        :param query_filter: filters for query.
        :return: models.
        """
        query = select(self.model)
        if query_filter is not None:
            query = query.filter(query_filter)
        return await paginate(self.session, query)

    async def get_by_id(self, id: str) -> Base:
        """
        Get a model by id.
        :param id: id of model.
        :return: a model.
        """
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")
        result_query = await self.session.execute(
            select(self.model).where(
                and_(
                    model_id == id,
                    self.model.deleted_at.is_(None),
                ),
            ),
        )

        try:
            return result_query.scalar_one()
        except NoResultFound:
            raise NoResultFound(f"{self.model.__name__} not found")

    async def update(
        self,
        query_filter: BinaryExpression,
        data_to_update: dict,
        force_multiple_updates: bool = False,
    ) -> int:
        """Update a model model by criteria.
        :param query_filter: criteria of model to update.
        :param data_to_update: dict with new data to update a model.
        :param force_multiple_updates: if set True, allow multiples updates.
        :return: count of rows to updated.
        :raises NoResultFound: if not found
        :raises AssertionError: if not update
        """
        result_query = await self.session.execute(
            update(self.model).where(query_filter).values(data_to_update),
        )
        if result_query.rowcount == 0:
            raise NoResultFound(f"{self.model.__name__} not found")
        if not force_multiple_updates and result_query.rowcount > 1:
            await self.session.rollback()
            raise AssertionError("More than one row is being changed")
        return result_query.rowcount

    async def update_by_id(self, id, data_to_update):
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")
        await self.update((model_id == id), data_to_update)

    async def _soft_delete(
        self,
        query_filter,
        data_to_update: dict,
        force_multiple_updates: bool = False,
    ) -> None:
        return await self.update(
            query_filter,
            data_to_update,
            force_multiple_updates,
        )

    async def soft_delete_by_id(
        self,
        id: str,
        data_to_update: dict = {"deleted_at": func.now()},
    ) -> None:
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")
        await self._soft_delete((model_id == id), data_to_update)
