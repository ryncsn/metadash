"""
Like some kind of dependency injection, but not exactly.
Have a differeng pattern.
Doc come later.
Explict, using decorator.
"""

from metadash.models.base import EntityModel
from typing import ClassVar

PROVIDERS = {}
PENDING_EXTENDS = {}

ATTR_PREFIX = "__md_srv_"
# TODO: Aware of what attribute is provided
# TODO: Warn on not initialized service
# TODO: Life cycle


class NoServiceError(Exception):
    pass


def use(provider):
    # TODO: "watch": property based / "on": event based / "use": progress bases
    """
    A middle ware registry function
    @on("testcase", "save")
    def func(entity, ...)
        // Will be called after testcase's every non-extended property saved successfully
        pass

    @on("testcase.result", "save")
    def func(entity, ...)
        // Will be called after testcase result saved
        // if result is not a provider registry, it will still work, after test case saved
        pass
    """
    pass


def _split_provider_extend(name: str):
    splitted_name = name.split(".")
    if len(splitted_name) == 1:
        return name, None
    elif len(splitted_name) == 2:
        return splitted_name[0], splitted_name[1]
    else:
        raise RuntimeError('Illegal provider name {}'.format(name))


def provide(name: str):
    """
    A Classes that provide a service.

    Provide a service with name in format <service_name>, provider must be a EntityModel
    Extend a service with name in format <service_name.extend_name>, provider must be
    a Class with attr (get/set) or (__get__/__set__)

    All happens in model layer.
    API layer could check if a attr exists by calling require().

    (Currently) Only called when model layer is initilizing
    """
    def fn(provider: ClassVar):
        # TODO: provider should inherit something?
        provider_name, extend_name = _split_provider_extend(name)
        if extend_name:
            return _provider_extend(provider_name, extend_name, provider)
        else:
            _provider_regist(provider_name, provider)
        return provider
    return fn


def require(name: str, **kwargs) -> ClassVar:
    """
    A service that provide some interface
    """
    # provider_name, extend_name = _split_provider(name)
    service = PROVIDERS.get(name, None)
    if not service:
        raise NoServiceError('No such service: {}'.format(name))
    for key, value in kwargs:
        if getattr(service, "__md_srv__{}".format(key)) != value:
            raise NoServiceError()
    provider_name, extend_name = _split_provider_extend(name)
    return service


def _provider_regist(provider_name: str, cls: ClassVar):
    """
    A service that provide some interface
    """
    service = PROVIDERS.setdefault(provider_name, cls)
    if service != cls:
        raise RuntimeError("Already exist: {}".format(provider_name))  # FIXME: exception type
    extends = PENDING_EXTENDS.pop(service, None)
    if extends:
        for attr, cls in extends:
            setattr(service, attr, cls)


def _provider_extend(provider_name: str, extend_name: str, cls: ClassVar,
                     serializable: bool=True, queryable: bool=False, sql: bool=False) -> None:
    """
    Extend a service with a Fn that provides a attr
    (Currently) only happend when model layer is initilizing
    """

    if serializable is False:
        # TODO: any idea about non serializable injection?
        raise NotImplementedError()
    if queryable is True:
        # TODO: if query is true, can be called with .<attr>().filter()?
        raise NotImplementedError()
    if sql is True and not isinstance(cls, EntityModel):
        # TODO: I guess we can inject some attribute using sqlalchemy object,
        # Something like a associateProxy, detect the relation and
        # wrap get/set?
        raise NotImplementedError()

    if sql:
        def _sql_get_wrap(self, *args, **kwargs):
            pass

        def _sql_set_wrap(self, *args, **kwargs):
            pass

    setattr(cls, "{}_sql".format(ATTR_PREFIX), sql)
    setattr(cls, "{}_queryable".format(ATTR_PREFIX), queryable)
    setattr(cls, "{}_serializable".format(ATTR_PREFIX), serializable)

    if sql:
        setattr(cls, "__get__", _sql_get_wrap)
        setattr(cls, "__set__", _sql_get_wrap)

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

    # TODO: cls should inherit something, using simple duck type check now
    def regist(cls):
        service = PROVIDERS.get(provider_name)
        if not service:
            PENDING_EXTENDS.setdefault(provider_name, []).append(cls)
        else:
            setattr(service, extend_name, cls)

    return regist
