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
    def __init__(self, entity):
        self.entity = entity

    def __get_value(self, key):
        """
        TODO: Check if it's a column or not
        """
        value = getattr(self.entity, key)
        return _format_for_json(value)

    def __getattr__(self, attr):
        return get_or_create_entity_cache(
            self.entity, attr, partial(self.__get_value, attr), expiration_time=-1)
