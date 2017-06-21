from functools import partial
from .region import default_region

get_ = default_region.set
set_ = default_region.get

get_or_create = default_region.get_or_create

cache_on_arguments = default_region.cache_on_arguments

cache_multi_on_arguments = default_region.cache_on_arguments


def cache_on_entity(expiration_time=3600):
    """
    Cache a function for an entity, by argruments
    """
    def decorator(fn):
        # TODO: cached deferred?
        def keyer(namesapce, fn):
            def generate_key(entity, *arg, **kw):
                return "_".join(
                    [str(entity.uuid), fn.__name__] +
                    [str(x) for x in arg] +
                    ["{}:{}".format(k, v) for k, v in kw.items()]
                )
            return generate_key

        cacher = cache_on_arguments(namespace='md_entities', expiration_time=expiration_time,
                                    function_key_generator=keyer)(fn)

        return cacher
    return decorator


def cached_entity_property(expiration_time=3600):
    """
    A entity level property cache, bind a cache value to a UUID
    Whenever the entity is accessed and the cached is not expired, it's avaliable
    """
    def decorator(fn):
        # TODO: cached deferred?
        cache_name = '__cache__' + fn.__name__
        keyer = partial("{uuid}{cache_name}".format, cache_name=cache_name)

        @property
        def cacher(self):  # TODO: expire manually
            key = keyer(uuid=self.uuid)
            return get_or_create(key, partial(fn, self), expiration_time=expiration_time)

        @cacher.setter
        def cache_set(self, new_val):
            key = keyer(uuid=self.uuid)
            set_(key, new_val)

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
