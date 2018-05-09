import functools


def mapper_hook(mapper__init__):
    """
    Hook the __init__ method of Mapper, make it easier to track
    the ralation ship of Entity and Attribute
    """
    @functools.wraps(mapper__init__)
    def fn(self, entity, *args, **kwargs):
        ret = mapper__init__(self, entity, *args, **kwargs)
        return ret
    return fn
