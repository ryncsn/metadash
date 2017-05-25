"""
"""
import itertools
import operator
import weakref
from sqlalchemy import exc, orm, util
from sqlalchemy.orm import collections, interfaces
from sqlalchemy.sql import not_, or_


def composive_proxy(target_collection, composition, **kw):
    return ComposiveProxy(target_collection, composition, **kw)


class ComposeOp(object):
    """
    Compositor take a python object, which hava to be a dict
    of array make up by string or a single string.

    When it's a dict, key is perserved as keyword, but value will
    be take from the target object by attribute name.
    When it's a array, each element have to be a string, and will
    be transalated into target attributes.
    """
    # TODO: performance
    def __init__(comp):
        if isinstance(comp, dict):
            pass
        elif isinstance(comp, list):
            pass
        elif isinstance(comp, str):
            pass

    def apply(self, operation, target, *args, **kwargs):
        pass


COMPOSIVE_PROXY = util.symbol('COMPOSIVE_PROXY')


class ComposiveProxy(interfaces.InspectionAttrInfo):
    """A descriptor that presents a read/write view of an object attribute."""

    is_attribute = False
    extension_type = COMPOSIVE_PROXY

    def __init__(self, target_collection, composition):
        """
        """

        self.owning_class = None
        self.key = '_%s_%s_%s' % (
            type(self).__name__, target_collection, id(self))
        self.collection_class = None
