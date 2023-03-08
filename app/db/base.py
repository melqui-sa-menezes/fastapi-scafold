from datetime import datetime
from typing import Any, Tuple

from sqlalchemy import Column, DateTime, Table, func, text
from sqlalchemy.orm import as_declarative, declarative_mixin, declared_attr

from app.db.meta import meta


@declarative_mixin
class CreatedAtMixin:
    @declared_attr
    def created_at(cls):  # pylint: disable=E0213
        return Column(
            DateTime(timezone=True),
            default=datetime.now,
            server_default=func.now(),
        )


@declarative_mixin
class UpdatedAtMixin:
    @declared_attr
    def updated_at(cls):  # pylint: disable=E0213
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            default=datetime.now,
            onupdate=datetime.now,
        )


@declarative_mixin
class DeletedAtMixin:
    @declared_attr
    def deleted_at(cls):  # pylint: disable=E0213
        return Column(
            DateTime(timezone=True),
            default=None,
            server_default=text("NULL"),
        )


@as_declarative(metadata=meta)
class Base(CreatedAtMixin, UpdatedAtMixin, DeletedAtMixin):
    """
    Base for all models.
    It has some type definitions to
    enhance autocompletion.
    """

    __tablename__: str
    __table__: Table
    __table_args__: (Tuple[Any, ...])
