from uuid import UUID

from sqlalchemy.orm import Query
from sqlalchemy.sql.expression import and_

from app.models.models import Product


def product_query_parameters(
    product_id: UUID,
    name: str,
    description: str,
) -> Query:
    query = list()  # noqa: C408

    if product_id:
        query.append(Product.product_id == product_id)

    if name:
        query.append(Product.name.ilike(f'%{name}%'))

    if description:
        query.append(Product.description.ilike(f'%{description}%'))

    query.append(Product.deleted_at.is_(None))

    return and_(*query)
