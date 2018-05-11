import weakref
from .. import db


def _find_rmixin(bases):
    for cls in bases:
        if hasattr(cls, '__rmixin_registry__'):
            return cls
    return None


def is_sub_class(cls):
    return issubclass(cls, cls.__rmixin_classref__())


def get_registed_subclasses(cls):
    return cls.__rmixin_registry__


class RichMixinMeta(type(db.Model)):  # Inherit from db.Model to work with flask-sqlalchemy
    """
    A Declarative Meta provides many feature used by this project.

    Allow us to:
    * Provide a skeleton class for reference and hinting
    * Attributes and properties from skeleton class is inherited by default, but
      won't be mapped
    * Make it easier to add properties and attributes at runtime (Execute hook when subclass is defined)
    * Track the subclasses of a mixin
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_):
        if not hasattr(cls, '__rmixin_classref__'):
            # Base class
            type.__init__(cls, classname, bases, dict_)
            cls.__rmixin_classref__ = weakref.ref(cls)
        else:
            cls.__rmixin_registry__[classname] = cls
            super(RichMixinMeta, cls).__init__(classname, bases, dict_)
            rmixin_class = cls.__rmixin_classref__()
            rmixin_class.sub_init(rmixin_class, cls, classname, bases, dict_)

    def __new__(mcs, classname, bases, dict_):
        rmixin_class = _find_rmixin(bases)
        # TODO: slot
        if rmixin_class is None:
            # Base class
            rmixin_defaults = dict(dict_)
            rmixin_registry = rmixin_defaults.pop('rmixin_registry', weakref.WeakValueDictionary())
            sub_new = rmixin_defaults.pop('sub_new', mcs.sub_new)
            sub_init = rmixin_defaults.pop('sub_init', mcs.sub_init)

            dict_['sub_new'] = sub_new
            dict_['sub_init'] = sub_init
            dict_['__rmixin_registry__'] = rmixin_registry
            dict_['__rmixin_defaults__'] = rmixin_defaults
            dict_['__rmixin_bases__'] = bases
        else:
            # Sub class
            defaults = rmixin_class.__rmixin_defaults__.copy()
            defaults.update(dict_)
            dict_ = defaults
            bases = (rmixin_class, ) + rmixin_class.__rmixin_bases__

            sub_new = rmixin_class.sub_new
            sub_new(rmixin_class, classname, bases, dict_)

        return super(RichMixinMeta, mcs).__new__(mcs, classname, bases, dict_)

    def sub_init(baseclass, subclass, subclass_name, baseclasses, subclass_dict):
        """
        Wrapped __init__ function only apply to subclass
        """
        return subclass

    def sub_new(baseclass, subclass_name, baseclasses, subclass_dict):
        """
        Wrapped __new__ function only apply to subclass
        """
        pass
