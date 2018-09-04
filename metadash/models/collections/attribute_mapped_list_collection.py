"""
Extended From https://groups.google.com/forum/#!msg/sqlalchemy/2wkMVfWBHeQ/vyPd75VSyMQJ
"""

import operator

from sqlalchemy.orm.collections import collection, collection_adapter


class ProxyList(list):
    """
    A list, get a attribute of this list will turn the list in to a new list
    which contains a list of target value of all elements in this list.
    """
    def __init__(self, *args, **kwargs):
        self._creator = kwargs.pop('_creator', lambda x: x)
        self._collecion_adapter = kwargs.pop('_collecion_adapter', None)
        self._proxied_reference = kwargs.pop('_proxied_reference', None)
        super(ProxyList, self).__init__(*args, **kwargs)

    def _append_event(self, value, _sa_initiator=None):
        return self._collecion_adapter.fire_append_event(value, _sa_initiator)

    def _remove_event(self, value, _sa_initiator=None):
        return self._collecion_adapter.fire_remove_event(value, _sa_initiator)

    def __getattr__(self, name):
        """
        Suppose to be used with associate proxy
        """
        if name.startswith('_'):
            raise AttributeError()
        return ProxyList([getattr(i, name) for i in self],
                         _collecion_adapter=self._collecion_adapter,
                         _creator=self._creator,
                         _proxied_reference=self
                         )

    def append(self, value, _sa_initiator=None, event=True):
        if self._proxied_reference:
            self._proxied_reference.append(self._proxied_reference._creator(value),
                                           _sa_initiator, event)
        elif event is not False:
            value = self._append_event(value, _sa_initiator)
        list.append(self, value)

    def remove(self, value, _sa_initiator=None, event=True):
        if value in self:
            if event is not False:
                if self._proxied_reference:
                    idx = self.index(value)
                    self._proxied_reference.__delitem__(idx, _sa_initiator=_sa_initiator)
                else:
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

    def __delitem__(self, index, _sa_initiator=None):
        val = self[index]
        self._remove_event(val)
        list.__delitem__(self, index)

    def __setitem__(self, index, value):
        existing = self[index]
        if existing is not value:
            if self._proxied_reference:
                self._proxied_reference.__setitem__(
                    index, self._proxied_reference._creator(value))
            else:
                self._remove_event(existing)
                self._append_event(value)
            list.__setitem__(self, index, value)


def default_creator(key, value):
    raise NotImplementedError()


class CreatorProxy:
    """
    Return a function object which accept one argument value
    with the specific key.
    """

    def __init__(self, creator, key):
        self.creator = creator
        self.key = key

    def __call__(self, value):
        return self.creator(self.key, value)


class MappedAggregationCollection(dict):
    """
    Return value directly if there is only one value, else give a list

    Every value in this dict is a list, which make it possible to aggregate
    collection which have duplicated keys

    if always_use_list is set to False, when a key is unique, access it's value
    will return value itself. If a key is duplicated, access it's value will return
    a list of value sharing the same key.
    """
    def __init__(self, attr_name, creator=None, always_use_list=False):
        self.keyfunc = operator.attrgetter(attr_name)
        self.creator = creator or default_creator
        self.always_use_list = always_use_list  # TODO
        self.owning_class = None

        super(MappedAggregationCollection, self).__init__()

    def factory(self, key, *args, **kwargs):
        kwargs['_collecion_adapter'] = collection_adapter(self)
        kwargs['_creator'] = CreatorProxy(self.creator, key)
        return ProxyList(*args, **kwargs)

    @collection.appender
    def add(self, value, _sa_initiator=None):
        key = self.keyfunc(value)
        self.__getitem__(key, raw=True).append(value, _sa_initiator, event=False)

    @collection.remover
    def remove(self, value, _sa_initiator=None):
        key = self.keyfunc(value)
        self[key].remove(value, _sa_initiator, event=False)

    # def _set(self, items):
    #     bulk_appender = collection_adapter(self).bulk_appender()
    #     for key, value in items.items():
    #         self.__setitem__(key, value, bulk_appender)

    @collection.internally_instrumented
    def __setitem__(self, key, value, appender=None):
        appender = appender or collection_adapter(self).fire_append_event
        if isinstance(value, ProxyList):
            dict.__setitem__(self, key, value)
        elif isinstance(value, list):
            value_ = value.copy()
            for idx, item in enumerate(value_):
                value_[idx] = appender(item)
            dict.__setitem__(self, key, self.factory(key, value_))
        else:
            value_ = [appender(value)]
            dict.__setitem__(self, key, self.factory(key, value_))

    @collection.internally_instrumented
    def __delitem__(self, key):
        adapter = collection_adapter(self)
        if key in self:
            adapter.fire_remove_event(self[key], None)
            dict.__delitem__(self, key)

    def __getdefaultitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            value = self.factory(key)
            dict.__setitem__(self, key, value)
            return value

    def __getitem__(self, key, raw=False):
        if raw is True:
            return self.__getdefaultitem__(key)
        elif self.always_use_list:
            return self.__getdefaultitem__(key)
        elif key in self:
            item_list = self.__getdefaultitem__(key)
            if len(item_list) == 1 and not self.always_use_list:
                return item_list[0]
            else:
                return item_list
        else:
            raise KeyError(key)

    @collection.iterator
    def iterate(self):
        for collection_or_item in self.values():
            for item in collection_or_item:
                yield item

    @collection.converter
    def _convert(self, target):
        for collection_or_item in target.values():
            for item in collection_or_item:
                yield item

class CreatorFactory:
    """
    If value is a list, create a instance for each element in value list.

    If duplicate value in the list, get rid of it, it's supposed to have
    unique value.
    """

    def __init__(self, owning_cl):
        self.owning_cl = owning_cl

    def __call__(self, key, value):
        target_model = self.owning_cl
        if isinstance(value, list):
            return [target_model(key, value) for value in set(value)]
        else:
            return target_model(key, value)


class attribute_mapped_list_collection(object):
    """
    A dictionary-based collection type with attribute-based keying,
    similar to attribute_mapped_collection, but allow key value to be
    duplicated and in such case, will create a list containing all values.

    When used with associate_proxy, __proxy_args__ must be passed to associate_proxy
    as keyword argument, and `target_class` should be provided or this class should
    be an attribute of `target_class`. Else associate_proxy might try to initialize a
    `target_class` object with list as arguments when trying to assign a list to an key.

    And pass __proxy_args__ to associate_proxy will improve the performance with
    bulk insert.
    """
    target_class = None

    # TODO: noway to implement implicit bulk update yet
    # @staticmethod
    # def proxy_bulk_set(proxy, values):
    #     update = dict(
    #         (key, proxy._create(key, value)) for key, value in values.items())
    #     proxy.col._set(update)

    def __init__(self, attr_name, target_class=None, **kwargs):
        self.owning_class = target_class
        self.attr_name = attr_name
        self.extra_kwargs = kwargs
        self.creator = CreatorFactory(self.owning_class)
        self.__proxy_args__ = {
            'creator': self.creator,
            # 'proxy_bulk_set': self.proxy_bulk_set
        }

    def __get__(self, obj, class_):
        if self.owning_class is None:
            self.owning_class = class_ and class_ or type(obj)
            self.creator = CreatorFactory(self.owning_class)
            self.__proxy_args__ = {
                'creator': self.creator,
                # 'proxy_bulk_set': self.proxy_bulk_set
            }
        return self

    def __call__(self):
        if not self.owning_class:
            raise AttributeError('attribute_mapped_list_collection_attr '
                                 'should be used as an class\'s attribute')
        return MappedAggregationCollection(self.attr_name, creator=self.creator, **self.extra_kwargs)
