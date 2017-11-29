from functools import partial
from .utils import _format_for_json
from metadash.cache.manager import (
    get_or_create_entity_cache,
    get_or_create_entity_model_cache,
    clear_entity_cache,
    clear_entity_model_cache,
    set_entity_cache,
    set_entity_model_cache,
    get_entity_cache,
    get_entity_model_cache,
    del_entity_cache,
    del_entity_model_cache,
)


class EntityCacheManager(object):
    """
    A cache storage for each entity

    When trying to get an attribute from an entity
    if the attribute doesn't exists, will fallback to retrive
    the attribute from the entity, then store in the cache storage
    automatically.
    Will raise Exception if fallback failed or failed to format the
    value into json.
    """
    def __init__(self):
        self.instance = None
        self.model = None

    def __get__(self, instance, model):
        self.instance = instance
        self.model = model
        return self

    def __get_value(self, key):
        """
        Extract value from instance or model
        """
        if self.instance:
            try:
                value = getattr(self.instance, key)
            except AttributeError:
                raise AttributeError("Entity instance {} doesn't have attribute {}".format(self.instance, key))
            return _format_for_json(value)
        else:
            try:
                value = getattr(self.model, key)
            except AttributeError:
                raise AttributeError("Model {} doesn't have attribute {}".format(self.model, key))
            return _format_for_json(value)

    def get(self, attr):
        if self.instance is not None:
            return get_entity_cache(self.instance, attr)
        elif self.model is not None:
            return get_entity_model_cache(self.model, attr)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")

    def set(self, attr, value):
        if self.instance is not None:
            return set_entity_cache(self.instance, attr, value)
        elif self.model is not None:
            return set_entity_model_cache(self.model, attr, value)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")

    def get_or_create(self, attr, fn=None):
        """
        If attr is a property of the eneity, fn could be None,
        and cacher will try to retrive value from entity on miss
        """
        fn = fn or partial(self.__get_value, attr)
        if self.instance is not None:
            return get_or_create_entity_cache(
                self.instance, attr, fn, expiration_time=-1)
        elif self.model is not None:
            return get_or_create_entity_model_cache(
                self.model, attr, fn, expiration_time=-1)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")

    def delete(self, attr):
        if self.instance is not None:
            return del_entity_cache(self.instance, attr)
        elif self.model is not None:
            return del_entity_model_cache(self.model, attr)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")

    def clear(self):
        if self.instance is not None:
            clear_entity_cache(self.instance)
        elif self.model is not None:
            clear_entity_model_cache(self.model)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")
