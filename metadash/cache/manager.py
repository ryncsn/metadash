"""
Manage cache by entity / attribute
"""
from .region import default_region

get_ = default_region.get
set_ = default_region.set
delete_ = default_region.delete

get_or_create = default_region.get_or_create

cache_on_arguments = default_region.cache_on_arguments

cache_multi_on_arguments = default_region.cache_on_arguments


def entity_model_keyer(model, key):
    return "_nscache_{}_{}".format(model.__namespace__, key)


def entity_keyer(entity, key):
    return "_cache_{}_{}".format(entity.uuid, key)


def entity_model_rec_keyer(model):
    return "_nscacherec_{}".format(model.__namespace__)


def entity_rec_keyer(entity):
    return "_cacherec_{}".format(entity.uuid)


def entity_fn_wrapper(fn, expiration_time=None):
    def keyer(namesapce, fn):
        def generate_key(entity, *args, **kwargs):
            key = "_fncache_" + "_".join(
                [str(entity.uuid), fn.__name__] +
                [str(x) for x in args] +
                ["{}:{}".format(k, v) for k, v in kwargs.items()])
            record_entity_cache(entity, key)
            return key
        return generate_key
    cached_fn = cache_on_arguments(namespace='md_entities', expiration_time=expiration_time or -1,
                                   function_key_generator=keyer)(fn)
    return cached_fn


def entity_model_fn_wrapper(fn, expiration_time=None):
    def keyer(namesapce, fn):
        def generate_key(model, *args, **kwargs):
            key = "_fncache_" + "_".join(
                [str(model.__namespace__), fn.__name__] +
                [str(x) for x in args] +
                ["{}:{}".format(k, v) for k, v in kwargs.items()])
            record_entity_model_cache(model, key)
            return key
        return generate_key
    cached_fn = classmethod(cache_on_arguments(namespace='md_entities', expiration_time=expiration_time or -1,
                                               function_key_generator=keyer)(fn))
    return cached_fn


def get_or_create_entity_model_cache(model, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity model
    """
    entity_scoped_key = entity_model_keyer(model, key)
    cache_record_key = entity_model_rec_keyer(model)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return get_or_create(entity_scoped_key, *args, **kwargs)


def get_or_create_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = entity_keyer(entity, key)
    cache_record_key = entity_rec_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return get_or_create(entity_scoped_key, *args, **kwargs)


def get_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    scoped_key = entity_keyer(entity, key)
    return get_(scoped_key, *args, **kwargs)


def get_entity_model_cache(model, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    scoped_key = entity_model_keyer(model, key)
    return get_(scoped_key, *args, **kwargs)


def set_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = entity_keyer(entity, key)
    cache_record_key = entity_rec_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return set_(entity_scoped_key, *args, **kwargs)


def set_entity_model_cache(model, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = entity_model_keyer(model, key)
    cache_record_key = entity_model_rec_keyer(model)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return set_(entity_scoped_key, *args, **kwargs)


def del_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = entity_keyer(entity, key)
    delete_(entity_scoped_key, *args, **kwargs)


def del_entity_model_cache(model, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity model
    """
    entity_scoped_key = entity_model_keyer(model, key)
    delete_(entity_scoped_key, *args, **kwargs)


def record_entity_cache(entity, key):
    """
    Tell the cache manager an cache entry have been created for an entity
    """
    cache_record_key = entity_rec_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(key)
    return set_(cache_record_key, entity_cache_record)


def record_entity_model_cache(entity, key):
    """
    Tell the cache manager an cache entry have been created for an entity
    """
    cache_record_key = entity_model_rec_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(key)
    return set_(cache_record_key, entity_cache_record)


def clear_entity_model_cache(model):
    # Clean model caches
    cache_records = get_(entity_model_rec_keyer(model))
    if cache_records:
        for key in cache_records:
            delete_(key)


def clear_entity_cache(entity):
    """
    Clear belong to an entity and it's model
    """
    # Clean instance caches
    cache_records = get_(entity_rec_keyer(entity))
    if cache_records:
        for key in cache_records:
            delete_(key)
