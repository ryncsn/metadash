"""
Helper mostly for internal use
"""
from ... import logger
from functools import wraps
from sqlalchemy.ext.associationproxy import (
    _AssociationDict, _AssociationSet, _AssociationList)


def _extend_column_arg_patch():
    """
    Monkey patch for some custom kwargs.
    """
    from sqlalchemy.sql.schema import Column

    _origin_column_init = Column.__init__

    def _extend_attr(self, *args, **kwargs):
        self.unique_attribute = kwargs.pop('unique_attribute', False)
        _origin_column_init(self, *args, **kwargs)

    Column.__init__ = _extend_attr


def _all_leaf(cls):
    subs = cls.__subclasses__()
    return sum([_all_leaf(cls) for cls in subs], []) if subs else [cls]


def _all_leaf_class(cls):
    if cls.__subclasses__():
        return _all_leaf(cls)
    return []


def _get_table_name_dict(dict_):
    _tablename = dict_.get('__tablename__', None)
    _table = dict_.get('__table__', None)
    tablename = _tablename or _table.name
    assert tablename and isinstance(tablename, (str))
    return tablename


def _get_alias_dict(dict_):
    _alias = dict_.get('__alias__', None)
    _tablename = _get_table_name_dict(dict_)
    modelname = _alias or _tablename
    assert modelname and isinstance(modelname, (str))
    return modelname


def _pluralize(singular):
    # FIXME: it's wrong, totally
    if singular.endswith('y'):
        return "{}ies".format(singular[:-1])
    if singular.endswith('s'):
        return "{}es".format(singular)
    if singular.endswith('o'):
        return "{}es".format(singular)
    return "{}s".format(singular) if not singular.endswith('s') else singular  # FIXME


def _format_for_json(data):
    """Format into json and load lazy-loading attr to prevent stall"""
    if isinstance(data, (int, float, str)):
        return data
    elif isinstance(data, _AssociationDict):
        return dict(data)
    elif isinstance(data, _AssociationList):
        return list(data)
    elif isinstance(data, _AssociationSet):
        return list(data)
    elif isinstance(data, dict):
        return dict([(k, _format_for_json(v)) for k, v in data.items()])
    elif hasattr(data, 'as_dict'):
        return data.as_dict()
    elif hasattr(data, '__iter__'):
        return [_format_for_json(_value) for _value in data]
    else:
        return str(data)


def _iscacheable(entity, attribute):
    return (
        attribute in entity.__cacheable_attributes__
    )


class _Jsonable(object):
    # pylint: disable=no-member
    def as_dict(self, only=None, exclude=None, extra=None):
        """
        Format a model instance into json.
        """
        ret = {}
        for col_name in only or [c.name for c in self.__table__.columns] + (extra or []):
            if not exclude or col_name not in exclude:
                if _iscacheable(self, col_name):
                    ret[col_name] = self.cache.get_or_create(col_name)
                else:
                    ret[col_name] = _format_for_json(getattr(self, col_name))
        return ret


class hybridmethod(object):
    """
    High performance hybrid function wrapper
    """
    __slot__ = ['context', 'method', 'clsmethod']

    def __init__(self, func):
        self.clsmethod = self.method = wraps(func)(lambda *a, **kw: func(self.context, *a, **kw))

    def classmethod(self, func):
        """
        Function to call when calling with class
        """
        self.clsmethod = wraps(func)(lambda *a, **kw: func(self.context, *a, **kw))
        return self

    def __get__(self, instance, cls):
        if instance is None:
            self.context = cls
            return self.clsmethod
        self.context = instance
        return self.method
