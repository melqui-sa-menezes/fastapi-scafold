import logging

from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import and_, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncScalarResult, AsyncSession
from sqlalchemy.sql.elements import BinaryExpression
from starlette import status

from app.api.helpers.exception import HTTPError, IntegrityException
from app.db.base import Base


class BaseRepository:
    """Class for accessing model table."""

    def __init__(self, session: AsyncSession, model: Base):  # pragma: no cover
        self.session = session
        self.model = model
        logging.basicConfig(level=logging.WARNING)
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
    ) -> int:
        """Update a model model by criteria.
        :param query_filter: criteria of model to update.
        :param data_to_update: dict with new data to update a model.
        :return: count of rows to updated.
        :raises NoResultFound: if not found
        :raises AssertionError: if not update
        """
        try:
            result_query = await self.session.execute(
                update(self.model).where(query_filter).values(data_to_update),
            )
            if result_query.rowcount == 0:
                raise NoResultFound(f"{self.model.__name__} not found")
            return result_query.rowcount
        except IntegrityError as error:
            status_code = (
                status.HTTP_409_CONFLICT
                if "duplicate key" in error.args[0]
                else status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            raise HTTPError(
                status_code=status_code,
                error_message=f"{error.args[0].split('DETAIL')[-1]}",
            )

    async def update_by_id(self, id, data_to_update):
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")
        await self.update(
            and_(
                model_id == id,
                self.model.deleted_at.is_(None),
            ),
            data_to_update,
        )

    async def _soft_delete(
        self,
        query_filter,
        data_to_update: dict,
    ) -> int:
        query = select(self.model.deleted_at).where(query_filter)
        result = await self.session.execute(query)
        if result.scalar_one():
            return 1
        return await self.update(
            query_filter,
            data_to_update,
        )

    async def soft_delete_by_id(
        self,
        id: str,
        data_to_update: dict,
    ) -> None:
        data_to_update.update({"deleted_at": func.now()})
        model_id = getattr(self.model, f"{self.model.__tablename__}_id")
        await self._soft_delete((model_id == id), data_to_update)
