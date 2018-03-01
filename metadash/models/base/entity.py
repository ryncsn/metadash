"""
Helper to define Entity models.
"""
import uuid

from .utils import (
    _get_table_name_dict, _Jsonable, hybridmethod)

from metadash.models import db
from metadash.models.types import UUID
from metadash.models.base.cache_manager import EntityCacheManager

from sqlalchemy import event


Model = db.Model


URN = '123e4567-e89b-12d3-a456-426655440000'


class MetadashEntity(Model):
    """
    The table indexing all NS and UUID of all type of entities.

    NS: Used to identify which plugin/model a entity belongs to.
    UUID: Unique identifier
    """
    __tablename__ = "metadash_entity"
    __table_args__ = (
        db.UniqueConstraint('namespace', 'index_uuid', name='_metadash_entity_uc'),
    )
    __namespace_map__ = {}
    __namespace__ = uuid.uuid5(uuid.UUID(URN), __tablename__)

    namespace = db.Column(UUID(), index=True, nullable=False, primary_key=True)
    index_uuid = db.Column(UUID(), index=True, nullable=False, unique=True, primary_key=True,
                           default=uuid.uuid1)

    __mapper_args__ = {
        'polymorphic_on': namespace,
        'polymorphic_identity': __namespace__
    }


MetadashEntity.__namespace_map__[MetadashEntity.__namespace__] = MetadashEntity


def after_entity_update_hook(mapper, connection, entity):
    entity.cache.clear()


class EntityMeta(type(db.Model)):
    """
    Custom metaclass for creating new Entity.

    Add support for auto-generated namespace, hook to auto create/destory
    key in MetadashEntity table.

    Why create key in MetadashEntity table? To maintain the integrity and clean up
    gabage properties and make it easier to cache, and make it easier to create M2M metadata.

    TODO: Using other metacalss other than sqlalchemy.ext.declarative.api.DeclarativeMeta
    will break this.
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_):
        if classname == "EntityModel":
            type.__init__(cls, classname, bases, dict_)
            return

        super(EntityMeta, cls).__init__(classname, bases, dict_)
        MetadashEntity.__namespace_map__[cls.namespace] = cls

        # Clean cache on entity update
        event.listen(cls, 'after_delete', after_entity_update_hook)
        event.listen(cls, 'after_update', after_entity_update_hook)

    def __new__(mcs, classname, bases, dict_):
        if classname == 'EntityModel':
            return type.__new__(mcs, classname, bases, dict_)

        dict_ = dict(dict_)  # Make it writable

        has_primary_key = False

        for key, value in dict_.items():
            if isinstance(value, db.Column):
                if value.primary_key:
                    has_primary_key = True

        __namespace__ = dict_.get('__namespace__',
                                  uuid.uuid5(uuid.UUID(URN), _get_table_name_dict(dict_)))
        if isinstance(__namespace__, str):
            __namespace__ = uuid.uuid5(uuid.UUID(URN), __namespace__)

        assert isinstance(__namespace__, uuid.UUID)

        __mapper_args__ = dict_.get('__mapper_args__', {})
        __mapper_args__['polymorphic_identity'] = __namespace__  # TODO: Error on already set?

        dict_['uuid'] = db.Column(
            UUID(), db.ForeignKey(MetadashEntity.index_uuid, ondelete="CASCADE", onupdate="RESTRICT"),
            index=True, nullable=False, primary_key=not has_primary_key, default=uuid.uuid1
        )

        dict_['__namespace__'] = __namespace__
        dict_['__mapper_args__'] = __mapper_args__
        dict_['attribute_models'] = EntityModel.attribute_models.copy()

        return super(EntityMeta, mcs).__new__(
            mcs, classname, (EntityModel, _Jsonable, MetadashEntity), dict_)


# pylint: disable=no-member
# EntityMeta will plug _Jsonable, MetadashEntity in as super class
class EntityModel(metaclass=EntityMeta):
    """
    Entity Model base that provide support for convinient
    attribute access.

    namespace is hardcodes in each EntityModel and generated with
    uuid5(NS=URN, <tablename>) if not privided.

    Use hardcoded NS, each table have a NS.
    """
    # Don't create any sqlalchemy things here
    # This class is just a skeleton
    # TODO: Raise error on create

    __alias__ = None

    __cacheable_attributes__ = set()

    attribute_models = {}

    uuid = None  # Just a hint

    cache = EntityCacheManager()

    def identity(self):
        """
        Return namespace + uuid
        """
        return '{}:{}'.format(self.__namespace__, self.uuid)

    @classmethod
    def from_uuid(cls, uuid):
        entity = cls.query.filter(uuid == uuid).first()
        return entity

    @hybridmethod
    def from_dict(self, dict_):
        """
        Inflate the instance with dict
        """
        for k, v in dict_.items():
            setattr(self, k, v)
        return self

    @from_dict.classmethod
    def from_dict(cls, dict_):
        """
        Inflate the instance with dict
        """
        instance = cls()
        for k, v in dict_.items():
            setattr(instance, k, v)
        return instance

    def as_dict(self, only=None, exclude=None, extra=None):
        """
        Convert this intstance to a dict
        else, only columns are loaded
        """
        extra = extra or []
        for model in self.attribute_models.values():
            extra.append(model.ref_name)
        dict_ = super(EntityModel, self).as_dict(only=only, exclude=exclude, extra=extra)
        return dict_
