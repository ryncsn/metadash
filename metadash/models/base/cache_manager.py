from functools import partial
from .utils import _format_for_json
from metadash.cache.manager import get_or_create_entity_cache


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
        if self.model is not None:
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

    def __getattr__(self, attr):
        if self.instance:
            return get_or_create_entity_cache(
                self.instance, attr, partial(self.__get_value, attr), expiration_time=-1)
        elif self.model:
            return get_or_create_entity_cache(
                self.model.__namespace__, attr, partial(self.__get_value, attr), expiration_time=-1)
        else:
            raise RuntimeError("Unbonded Entity Cache Manager")
