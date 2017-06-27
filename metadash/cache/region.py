"""
Initialize the region
"""

from config import ActiveConfig
from dogpile.cache import make_region
from dogpile.cache.util import sha1_mangle_key
from metadash import logger

backend = ActiveConfig.CACHE_DEFAULT_BACKEND
arguments = ActiveConfig.CACHE_ARGUEMENTS


def flatten(obj, recusrsion=3):
    if recusrsion == 0:
        raise RuntimeError('For performance, recursion level is limited for flating')
    try:
        if isinstance(obj, (str, int, float)):
            return obj
        if isinstance(obj, dict):
            return '_'.join(['{}:{}'.format(k, flatten(v, recusrsion - 1))
                             for k, v in obj.items()])
        if isinstance(obj, list):
            return '_'.join(['{}'.format(flatten(v, recusrsion - 1))
                             for v in obj])
        else:
            raise RuntimeError('Unsupported Data Type: {}:{}'.format(type(obj), obj))
    except Exception:
        logger.error('Error mangling obj: {}'.format(obj))
        raise


def universal_key_mangler(key):
    return sha1_mangle_key(flatten(key).encode())


# A default region
default_region = make_region(key_mangler=universal_key_mangler).configure(
    backend,
    expiration_time=-1,
    arguments=arguments
)

# TODO: backend using redis
# storage = make_region().configure(
#     backend,
#     expiration_time=-1,
#     arguments={}
# )
