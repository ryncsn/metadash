from sqlalchemy import inspect
from sqlalchemy.util import duck_type_collection
from flask_restful import reqparse, inputs
from flask import request, g, jsonify
from datetime import datetime

from .. import logger


class FuncBool(object):
    """
    Return overlay_func's return value as bool, if return value
    is None, return default
    """
    def __init__(self, func, default):
        self.func = func
        self.default = default

    def __bool__(self):
        ret = self.func()
        return self.default if ret is None else ret

    __nonzero__ = __bool__


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
        self.relation_overlay = kw.pop('relation_overlay', False)
        self.ignore_required_on_get = kw.pop('ignore_required_on_get', True)
        super(EntityParser, self).__init__(*a, **kw)
        self.entity = entity
        self.lazy_initialized = False

    def default_required(self):
        if self.ignore_required_on_get and request.method in ('GET', 'PUT'):
            return False
        else:
            return None

    def initialize(self):
        if self.entity:
            columns = inspect(self.entity).columns
            relation_column = {}
            for relationship in inspect(self.entity).relationships:
                if len(relationship.local_columns):
                    column, = relationship.local_columns
                    relation_column[column.name] = relationship.key

            for column in columns:
                # TODO: better validation
                if column.name in ['namespace']:  # TODO: move this to columns defination
                    continue
                type_ = column.type.python_type
                if type_ == datetime:
                    type_ = inputs.datetime_from_iso8601
                self.add_argument(
                    column.name if (
                        not self.relation_overlay or column.name not in relation_column
                    ) else relation_column[column.name],
                    type=type_,
                    location=self.default_location,
                    store_missing=False,
                    required=FuncBool(self.default_required, column.default is None and not column.nullable),
                    dest=column.name
                )

            for attr in self.entity.attribute_models:
                duck_type = duck_type_collection(attr.__collector__())
                default = None

                # Don't give None on empty for compatibility with associate proxy
                action = 'store'
                if duck_type in (dict,):
                    default = duck_type()
                elif duck_type in (list, set):
                    type_ = duck_type
                    action = 'append'

                    def duck_type(x):
                        return x
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
                    action=action
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

    def parse_extra(self, *a, **kw):
        """
        Using with GET only, parse all extra aguements
        TODO: delclare property/tag explitily, limit/page is confusing
        """
        assert (request.method == 'GET')
        if not self.lazy_initialized:
            self.initialize()
        normal_arg_names = [arg.name for arg in self.args]
        extra_args = {}  # Use MultiDict
        for key, value in request.args.items():
            if key in normal_arg_names or key in ['limit', 'page']:
                continue
            extra_args.setdefault(key, []).append(value)
        return dict((k, v[0]) if len(v) == 1 else v for k, v in extra_args.items())


def pager(query, page=None, limit=None):
    """
    Apply limit and offset to a given SQLAlchemy query object
    """
    g.paged = True
    g.page = page = page or int(request.args.get('page') or 0)
    g.limit = limit = limit or int(request.args.get('limit') or 50)
    return query.limit(limit).offset(limit * page)


def envolop(data, **kw):
    """
    Envolop return value for jsonify, if pager was used, will add
    """
    url = request.url
    ret = {'data': data}
    count = len(data)  # TODO: what if data is not countable
    if hasattr(g, 'paged'):
        _ = '&' if request.args else '?'
        template = '{url}{_}limit={limit}&page={page}'
        page, limit = g.page, g.limit
        ret['prev'] = template.format(url=url, _=_, page=page - 1, limit=limit) if page else None
        ret['next'] = template.format(url=url, _=_, page=page + 1, limit=limit) if data and limit == count else None  # FIXME: no next when next page is not avaliable
    ret.update(kw)
    return jsonify(ret)


def jsonp(json, callback=None):
    callback = callback or request.args.get('callback') or request.args.get('_')
    if not callback:
        raise RuntimeError('No Callback for JSONP founded')
    return "{callback}({json})".format(callback=callback, json=json)
