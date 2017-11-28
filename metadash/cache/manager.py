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


def entity_model_keyer(entity, key):
    return "_nscache_{}_{}".format(entity.__namespace__, key)


def entity_keyer(entity, key):
    return "_cache_{}_{}".format(entity.uuid, key)


def entity_model_rec_keyer(entity):
    return "_nscacherec_{}".format(entity.__namespace__)


def entity_rec_keyer(entity):
    return "_cacherec_{}".format(entity.uuid)


def get_or_create_entity_model_cache(entity, key, *args, **kwargs):
    """
    Get or create cache item belongs to an entity model
    """
    entity_scoped_key = entity_keyer(entity, key)
    cache_record_key = entity_rec_keyer(entity)
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


def clear_entity_model_cache(entity):
    # Clean model caches
    cache_records = get_(entity_model_rec_keyer(entity))
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
    clear_entity_model_cache(entity)


def clear_attribute_cache(attribute):
    """
    Clear belong related to an attribute
    """
    for entity in attribute.__entities__:
        clear_entity_cache(entity)


def after_entity_update_hook(mapper, connection, target):
    uuid = target.uuid
    if target.__namespace__:  # Make sure not a dangling entity
        clear_entity_cache(target)
    if uuid:  # Make sure not a dangling entity
        clear_entity_cache(target)


def after_attribute_update_hook(mapper, connection, target):
    uuid = target.uuid
    if uuid:  # Not a dangling entity
        clear_entity_cache(target)
