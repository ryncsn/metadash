"""
Helper to define Entity models.
"""
import uuid
import weakref

from sqlalchemy import event
from sqlalchemy.orm import column_property

from .utils import (
    _get_table_name_dict, _Jsonable, hybridmethod)

from .. import db
from ..types import UUID
from .cache_manager import EntityCacheManager
from .registry import EntityRegistry, AttributeRegistry, SharedAttributeRegistry
from .rich_mixin_meta import RichMixinMeta


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
    __namespace_map__ = weakref.WeakValueDictionary()
    __namespace__ = uuid.uuid5(uuid.UUID(URN), __tablename__)

    namespace = db.Column(UUID(), index=True, nullable=False)
    index_uuid = db.Column(UUID(), index=True, nullable=False, unique=True, primary_key=True,
                           default=uuid.uuid1)

    __mapper_args__ = {
        'polymorphic_on': namespace,
        'polymorphic_identity': __namespace__
    }


MetadashEntity.__namespace_map__[MetadashEntity.__namespace__] = MetadashEntity


def after_entity_update_hook(mapper, connection, entity):
    entity.cache.clear()


# pylint: disable=no-member
class EntityModel(_Jsonable, MetadashEntity, metaclass=RichMixinMeta):
    """
    Entity Model base that provide support for convinient
    attribute access.

    namespace is hardcodes in each EntityModel and generated with
    uuid5(NS=URN, <tablename>) if not privided.

    Use hardcoded NS, each table have a NS.
    """
    rmixin_registry = EntityRegistry

    # Don't create any sqlalchemy things here
    # This class is just a skeleton, for hinting
    # TODO: Raise error on create

    __alias__ = None

    __cacheable_attributes__ = set()

    attribute_models = weakref.WeakValueDictionary()

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

    # pylint: disable=no-self-argument
    def sub_init(baseclass, subclass, subclass_name, baseclasses, subclass_dict):
        for a_entity in AttributeRegistry.values():
            a_entity.build_relationship(a_entity)
        for sa_entity in SharedAttributeRegistry.values():
            sa_entity.build_relationship(sa_entity)

        # TODO: move it
        for key, value in subclass_dict.items():
            if hasattr(value, '__cached_property'):
                subclass.__cacheable_attributes__.add(getattr(value, '__cached_property'))

        MetadashEntity.__namespace_map__[subclass.__namespace__] = subclass
        # Clean cache on entity update
        event.listen(subclass, 'after_delete', after_entity_update_hook)
        event.listen(subclass, 'after_update', after_entity_update_hook)

    def sub_new(baseclass, subclass_name, baseclasses, subclass_dict):
        has_primary_key = False

        for key, value in subclass_dict.items():
            if isinstance(value, db.Column):
                if value.primary_key:
                    has_primary_key = True

        __namespace__ = subclass_dict.get('__namespace__',
                                          uuid.uuid5(uuid.UUID(URN), _get_table_name_dict(subclass_dict)))

        if isinstance(__namespace__, str):
            __namespace__ = uuid.uuid5(uuid.UUID(URN), __namespace__)

        assert isinstance(__namespace__, uuid.UUID)

        __mapper_args__ = subclass_dict.get('__mapper_args__', {})
        __mapper_args__['polymorphic_identity'] = __namespace__  # TODO: Error on already set?

        subclass_dict['uuid'] = db.Column(
            UUID(), db.ForeignKey(MetadashEntity.index_uuid),
            index=True, nullable=False, primary_key=not has_primary_key, default=uuid.uuid1
        )

        subclass_dict['__cacheable_attributes__'] = set()
        subclass_dict['__namespace__'] = __namespace__
        subclass_dict['__mapper_args__'] = __mapper_args__
        subclass_dict['attribute_models'] = weakref.WeakValueDictionary()


# pylint: disable=no-member
class BareEntityModel(_Jsonable, MetadashEntity, metaclass=RichMixinMeta):
    """
    A entiry with no local storage/database,
    Used to reference to remote data.

    Need to provide a __namespace__ to identify it.
    __namespace__ should be either a UUID or a string, which will be
    hashed into a uuid5.
    """
    rmixin_registry = EntityRegistry

    # Don't create any sqlalchemy things here
    # This class is just a skeleton
    # TODO: Raise error on create

    __alias__ = None

    __cacheable_attributes__ = set()

    attribute_models = weakref.WeakValueDictionary()

    def identity(self):
        return '{}:{}(bare)'.format(self.__namespace__, self.uuid)

    def as_dict(self, only=None, exclude=None, extra=None):
        extra = extra or []
        for model in self.attribute_models.keys():
            extra.append(model.ref_name)
        dict_ = super(BareEntityModel, self).as_dict(only=only, exclude=exclude, extra=extra)
        return dict_

    def sub_init(baseclass, subclass, subclass_name, baseclasses, subclass_dict):
        setattr(subclass, 'uuid', column_property(MetadashEntity.index_uuid))
        for a_entity in AttributeRegistry.values():
            a_entity.build_relationship(a_entity)
        for sa_entity in SharedAttributeRegistry.values():
            sa_entity.build_relationship(sa_entity)

        MetadashEntity.__namespace_map__[subclass.__namespace__] = subclass

    def sub_new(baseclass, subclass_name, baseclasses, subclass_dict):
        __namespace__ = subclass_dict.get('__namespace__', None)
        if isinstance(__namespace__, str):
            __namespace__ = uuid.uuid5(uuid.UUID(URN), __namespace__)
        assert isinstance(__namespace__, uuid.UUID)

        __mapper_args__ = subclass_dict.get('__mapper_args__', {})
        __mapper_args__['polymorphic_identity'] = __namespace__
        # TODO: Error on already set?

        # pylint: disable=no-member
        subclass_dict['__cacheable_attributes__'] = set()
        subclass_dict['__table__'] = MetadashEntity.__table__
        subclass_dict['__namespace__'] = __namespace__
        subclass_dict['__mapper_args__'] = __mapper_args__
        subclass_dict['attribute_models'] = weakref.WeakValueDictionary()
