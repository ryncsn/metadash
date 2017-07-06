from sqlalchemy import inspect
from sqlalchemy.util import duck_type_collection
from flask_restful import reqparse
from flask import request, g, jsonify

from .. import logger


class EntityParser(reqparse.RequestParser):
    """
    A wrapper flask-restful parser, for entity

    Lazy initialize to ensure inspect is not called until
    attributes are initialized.

    If this parser is initialize before attributes are initialized,
    thing may go wrong. *TODO*
    """
    def __init__(self, entity, *a, **kw):
        kw.setdefault('bundle_errors', True)
        self.default_location = kw.pop('location', [])
        super(EntityParser, self).__init__(*a, **kw)
        self.entity = entity
        self.lazy_initialized = False

    def initialize(self):
        if self.entity:
            columns = inspect(self.entity).columns
            relationships = inspect(self.entity).relationships
            print([str(i) for i in columns])
            print([str(i) for i in relationships])
            for column in columns:
                # TODO: better validation
                self.add_argument(
                    column.name,
                    type=column.type.python_type,
                    location=self.default_location,
                    store_missing=False,
                    required=(column.default is None and not column.nullable)
                )

            for attr in self.entity.attribute_models:
                duck_type = duck_type_collection(attr.__collector__())
                default = None

                # Don't give None on empty for compatibility with associate proxy
                if duck_type in (list, dict, set):
                    default = duck_type()
                else:
                    default = None

                if not duck_type:
                    logger.error('Unsupported attribute collection for attribute: {}'.format(attr))

                self.add_argument(
                    attr.ref_name,
                    type=duck_type,
                    location=self.default_location,
                    store_missing=False,
                    default=default,
                )

    def parse_args(self, *a, **kw):
        if not self.lazy_initialized:
            self.initialize()
        self.default_location.clear()
        if request.method == 'GET':
            self.default_location.extend(['args'])
        elif request.method == 'POST' or request.method == 'PUT':
            self.default_location.extend(['json'])
        return super(EntityParser, self).parse_args(*a, **kw)



def pager(query, page=None, limit=None):
    """
    Apply limit and offset to a given SQLAlchemy query object
    """
    g.paged = True
    g.page = page = page or request.args.get('page') or 0
    g.limit = limit = limit or request.args.get('limit') or 50
    return query.limit(limit).offset(limit * page)


def envolop(data, **kw):
    """
    Envolop return value for jsonify, if pager was used, will add
    """
    url = request.url
    ret = {'data': data}
    if hasattr(g, 'paged'):
        _ = '&' if request.args else '?'
        template = '{url}{_}limit={limit}&page={page}'
        page, limit = g.page, g.limit
        ret['prev'] = template.format(url, _, page=page - 1, limit=limit) if page else None
        ret['next'] = template.format(url, _, page=page - 1, limit=limit) if data else None  # FIXME: no next when next page is not avaliable
    ret.update(kw)
    return jsonify(ret)


def jsonp(json, callback=None):
    callback = callback or request.args.get('callback') or request.args.get('_')
    if not callback:
        raise RuntimeError('No Callback for JSONP founded')
    return "{callback}({json})".format(callback=callback, json=json)
