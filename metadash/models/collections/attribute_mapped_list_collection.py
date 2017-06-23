"""
Extended From https://groups.google.com/forum/#!msg/sqlalchemy/2wkMVfWBHeQ/vyPd75VSyMQJ
"""

import collections
import operator

from sqlalchemy.orm.collections import collection, collection_adapter


class ProxyList(list):
    """
    A list, get a attribute of this list will turn the list in to a new list
    which contains a list of target value of all elements in this list.
    """
    def __init__(self, *args, **kwargs):
        self._collecion_adapter = kwargs.pop('_collecion_adapter', None)
        super(ProxyList, self).__init__(*args, **kwargs)

    def _append_event(self, value, _sa_initiator=None):
        return self._collecion_adapter.fire_append_event(value, _sa_initiator)

    def _remove_event(self, value, _sa_initiator=None):
        return self._collecion_adapter.fire_remove_event(value, _sa_initiator)

    def __getattr__(self, name):
        """
        Suppose to be used with associate proxy
        """
        if not name.startswith('_'):
            return [getattr(item, name) for item in self]
        else:
            raise AttributeError()

    def append(self, value, _sa_initiator=None):
        value = self._append_event(value, _sa_initiator)
        list.append(self, value)

    def remove(self, value, _sa_initiator=None):
        self._remove_event(value, _sa_initiator)
        list.remove(self, value)

    def pop(self, _sa_initiator=None):
        value = list.pop(self)
        self._remove_event(value, _sa_initiator)
        return value

    def insert(self):
        raise NotImplementedError()

    def extend(self):
        raise NotImplementedError()

    def __delitem__(self, index):
        val = self[index]
        self._remove_event(val)
        list.__delitem__(self, index)

    def __setitem__(self, index, value):
        existing = self[index]
        if existing is not value:
            self._remove_event(existing)
            self._append_event(value)
            list.__setitem__(self, index, value)


class MaappedAggregationCollection(collections.defaultdict):
    """
    Return value directly if there is only one value, else give a list
    """
    def __init__(self, keyfunc, always_use_list=False):
        super(MaappedAggregationCollection, self).__init__(
            lambda: ProxyList(_collecion_adapter=collection_adapter(self)))
        self.keyfunc = keyfunc
        self.always_use_list = always_use_list  # TODO

    @collection.appender
    def add(self, value, _sa_initiator=None):
        key = self.keyfunc(value)
        self.__getitem__(key, raw=True).append(value, _sa_initiator)

    @collection.remover
    def remove(self, value, _sa_initiator=None):
        key = self.keyfunc(value)
        self[key].remove(value, _sa_initiator)

    @collection.internally_instrumented
    def __setitem__(self, key, value):
        if not isinstance(value, list):
            value = [value]
        adapter = collection_adapter(self)
        for item in value:
            item = adapter.fire_append_event(item, None)
        collections.defaultdict.__setitem__(self, key, value)

    @collection.internally_instrumented
    def __delitem__(self, key, value):
        adapter = collection_adapter(self)
        for item in value:
            item = adapter.fire_remove_event(item, None)
        collections.defaultdict.__delitem__(self, key, value)

    def __getitem__(self, key, raw=False):
        collection_or_item = collections.defaultdict.__getitem__(self, key)
        if len(collection_or_item) == 1 and not self.always_use_list and not raw:
            return collection_or_item[0]
        return collection_or_item

    @collection.iterator
    def iterate(self):
        for collection_or_item in self.values():
            if isinstance(collection_or_item, (list, set)):
                for item in collection_or_item:
                    yield item
            else:
                yield collection_or_item

    @collection.converter
    def _convert(self, target):
        for collection_or_item in target.values():
            if isinstance(collection_or_item, (list, set)):
                for item in collection_or_item:
                    yield item
            else:
                yield collection_or_item


def attribute_mapped_list_collection(attr_name):
    """A dictionary-based collection type with attribute-based keying.

    Returns a :class:`.MappedCollection` factory with a keying based on the
    'attr_name' attribute of entities in the collection, where ``attr_name``
    is the string name of the attribute.

    The key value must be immutable for the lifetime of the object.  You
    can not, for example, map on foreign key values if those key values will
    change during the session, i.e. from None to a database-assigned integer
    after a session flush.

    """
    getter = operator.attrgetter(attr_name)
    return lambda: MaappedAggregationCollection(getter)
