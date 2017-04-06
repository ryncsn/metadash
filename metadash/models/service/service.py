"""
Like some kind of dependency injection
"""

SERVICES = {}
EXTENDS = {}
# TODO: Aware of what attribute is provided
# TODO: Warn on not initialized service
# TODO: Life cycle


def provide(name):
    """
    A Fn that provide a service or attribute for service
    """
    # TODO: cls should inherit something
    def regist(cls):
        SERVICES[name] = cls
    return regist


def extend(serv, attr, serializable=True, queryable=False, sql=False):
    """
    A Fn that provide a attr for an service
    """
    if not serializable:
        # TODO: So many TODOs XD
        raise NotImplementedError()
    if queryable:
        raise NotImplementedError()
    if sql:
        raise NotImplementedError()

    # TODO: cls should inherit something, using simple duck type check now
    def regist(cls):
        if not hasattr(cls, "__get__"):
            if hasattr(cls, "get"):
                setattr(cls, "__get__", cls.get)
            else:
                raise RuntimeError()  # FIXME

        if not hasattr(cls, "__set__"):
            if hasattr(cls, "set"):
                setattr(cls, "__set__", cls.get)
            else:
                raise RuntimeError()  # FIXME
        service = EXTENDS.setdefault(serv, {})
        service[attr] = cls

    return regist


def require(need):
    """
    A service that provide some interface
    """
    service = SERVICES[need]
    extends = EXTENDS.pop(service, None)
    if extends:
        for attr, cls in extends:
            setattr(service, attr, cls)
