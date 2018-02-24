from functools import partial
from .region import default_region
from .manager import (
    get_or_create_entity_cache,
    set_entity_cache,
    entity_fn_wrapper,
    entity_model_fn_wrapper)

# append a _ to avoid namespace conflict
get_ = default_region.get
set_ = default_region.set
delete_ = default_region.delete
# To use dogpile's distributed lock support
get_mutex = default_region.backend.get_mutex

get_or_create = default_region.get_or_create

cache_on_arguments = default_region.cache_on_arguments

cache_multi_on_arguments = default_region.cache_on_arguments


def cache_on_entity(expiration_time=-1):
    """
    Cache a function for an entity, by argruments
    """
    def decorator(fn):
        return entity_fn_wrapper(fn, expiration_time)
    return decorator


def cache_on_entity_model(expiration_time=-1):
    """
    Cache a function for an entity model, by argruments
    """
    def decorator(fn):
        return entity_model_fn_wrapper(fn, expiration_time)
    return decorator


def cached_entity_property(expiration_time=-1):
    """
    A entity level property cache, bind a cache value to a UUID
    Whenever the entity is accessed and the cached is not expired, it's avaliable
    """
    def decorator(fn):
        # TODO: cached deferred?
        cache_name = fn.__name__

        @property
        def cacher(self):  # TODO: expire manually
            # assert isinstance(self, Entity)
            return get_or_create_entity_cache(
                self, cache_name, partial(fn, self), expiration_time=expiration_time)

        @cacher.setter
        def cache_set(self, new_val):
            return set_entity_cache(self, cache_name, new_val)

        return cacher
    return decorator


def cached_property(fn):
    """
    A pure python cached property, as a property belong to a single object,
    this cache only work for a single object and expire when object if freed.
    Always memory only.
    """
    # TODO: cached deferred?
    cache_name = '__cache__' + fn.__name__

    @property
    def cache_eval(self):
        if not hasattr(self, cache_name):
            value = fn(self)
            setattr(self, '{}_expire'.format(fn.__name__),  # TODO naming conflict?
                    lambda: delattr(self, cache_name))
            setattr(self, cache_name, value)
        return getattr(self, cache_name)

    @cache_eval.setter
    def cache_set(self, new_val):
        setattr(self, cache_name, new_val)

    return cache_eval
