"""
Helper to define remote models.

Remove model don't have a standalone local table
"""
import uuid

from metadash.models import db, UUID, get_or_create, get
from metadash.models.base import URN, MetadashEntity, _Jsonable
from metadash import logger


class MetadashRemoteEntityMeta(db.Model):
    """
    Remote entity
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_):
        if classname == "RemoteModel":
            type.__init__(cls, classname, bases, dict_)
            return

        # TODO
        MetadashEntity.__namespace_map__[cls.namespace] = cls
        raise NotImplementedError()

    # pylint: disable=no-member
    def __new__(mcs, classname, bases, dict_):
        if classname == 'RemoteModel':
            return type.__new__(mcs, classname, bases, dict_)

        dict_ = dict(dict_) # Make it writable

        assert isinstance(dict_['namespace'], uuid.UUID)

        dict_['__table__'] = MetadashEntity.__table__

        return super(MetadashRemoteEntityMeta, mcs).__new__(mcs, classname, bases, dict_)


class RemoteModel(_Jsonable, db.Model, metaclass=MetadashRemoteEntityMeta):
    __alias__ = None

    attribute_models = []

    def identity(self):
        return '{}:{}'.format(self.namespace, self.uuid)
