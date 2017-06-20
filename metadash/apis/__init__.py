import uuid

from sqlalchemy.util import duck_type_collection
from flask_restful import reqparse

from .. import logger


def default_entity_parser(entity=None):
    """
    Return a parser support parsing attributes and some basic columns
    TODO: validation
    """
    EntityParser = reqparse.RequestParser(bundle_errors=True)
    if entity:
        for column in entity.__table__.c:
            EntityParser.add_argument(
                column.name,
                type=column.type.python_type,
                location='json',
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
