from sqlalchemy.util import duck_type_collection
from flask_restful import reqparse
from flask import request, g, jsonify

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
    g['paged'] = True
    g['page'] = page = page or request.args.get('page') or 0
    g['limit'] = limit = limit or request.args.get('limit') or 50
    return query.limit(limit).offset(limit * page)


def envolop(data, **kw):
    """
    Envolop return value for jsonify, if pager was used, will add
    """
    url = request.url
    ret = {'data': data}
    if g.get('paged'):
        _ = '&' if request.args else '?'
        template = '{url}{_}limit={limit}&page={page}'
        page, limit = g['page'], g['limit']
        ret['prev'] = template.format(url, _, page=page - 1, limit=limit) if page else None
        ret['next'] = template.format(url, _, page=page - 1, limit=limit) if data else None  # FIXME: no next when next page is not avaliable
    ret.update(kw)
    return jsonify(ret)


def jsonp(json, callback=None):
    callback = callback or request.args.get('callback') or request.args.get('_')
    if not callback:
        raise RuntimeError('No Callback for JSONP founded')
    return "{callback}({json})".format(callback=callback, json=json)
