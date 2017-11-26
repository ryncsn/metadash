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


def cache_record_keyer(entity):
    return "{}__cacherecord__".format(entity.uuid)


def get_or_create_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = "{}__cache__{}".format(entity.uuid, key)
    cache_record_key = cache_record_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return get_or_create(entity_scoped_key, *args, **kwargs)


def set_entity_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity
    """
    entity_scoped_key = "{}{}".format(entity.uuid, key)
    cache_record_key = cache_record_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(entity_scoped_key)
    set_(cache_record_key, entity_cache_record)
    return set_(entity_scoped_key, *args, **kwargs)


def record_entity_cache(entity, key):
    """
    Tell the cache manager an cache entry have been created for an entity
    """
    cache_record_key = cache_record_keyer(entity)
    entity_cache_record = get_or_create(cache_record_key, lambda: [], -1)
    entity_cache_record.append(key)
    return set_(cache_record_key, entity_cache_record)


def clear_entity_cache(entity):
    """
    Clear belong to an entity
    """
    cache_record_key = cache_record_keyer(entity)
    cache_records = get_(cache_record_key)
    if cache_records:
        for key in cache_records:
            delete_(key)


def clear_attribute_cache(attribute):
    """
    Clear belong related to an attribute
    """
    for entity in attribute.__entities__:
        cache_record_key = cache_record_keyer(entity)
        cache_records = get_(cache_record_key)
        if cache_records:
            for key in cache_records:
                delete_(key)


def after_entity_update_hook(mapper, connection, target):
    uuid = target.uuid
    if uuid:  # Not a dangling entity
        clear_entity_cache(target)


def after_attribute_update_hook(mapper, connection, target):
    uuid = target.uuid
    if uuid:  # Not a dangling entity
        clear_entity_cache(target)
