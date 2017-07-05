from sqlalchemy.util import duck_type_collection
from flask_restful import reqparse
from flask import request

from .. import logger


def default_entity_parser(entity=None, location=None):
    """
    Return a parser support parsing attributes and some basic columns
    TODO: validation
    """
    location = location or ['args', 'json']
    EntityParser = reqparse.RequestParser(bundle_errors=True)
    if entity:
        for column in entity.__table__.c:
            EntityParser.add_argument(
                column.name,
                type=column.type.python_type,
                location=location,
                required=(column.default is None and not column.nullable)
            )

        for attr in entity.attribute_models:
            duck_type = duck_type_collection(attr.__collector__())
            default = None

            # Don't give None on empty for compatibility with associate proxy
            if duck_type in (list, dict, set):
                default = duck_type()
            else:
                default = None

            if not duck_type:
                logger.error('Unsupported attribute collection for attribute: {}'.format(attr))
            EntityParser.add_argument(
                attr.ref_name,
                type=duck_type,
                location='json',
                default=default,
            )
    return EntityParser


def pager(query, page=None, limit=None):
    """
    Apply limit and offset to a given SQLAlchemy query object
    """
    page = page or request.args.get('page') or 0
    limit = limit or request.args.get('limit') or 50

    return query.limit(limit).offset(limit * page)
