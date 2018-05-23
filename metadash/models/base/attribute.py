"""
Helper to define attribute/metadata models.
"""
import uuid

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, foreign, remote
from sqlalchemy.ext.associationproxy import association_proxy
from .utils import _get_alias_dict

from ..types import UUID
from .. import db

from metadash.event import on
from metadash.utils import pluralize
from .entity import MetadashEntity, EntityModel
from .utils import _get_alias_dict, _get_table_name_dict
from .utils import _Jsonable, _format_for_json
from .rich_mixin_meta import RichMixinMeta

from .registry import AttributeRegistry
from .registry import SharedAttributeRegistry
from .registry import EntityRegistry


Model = db.Model


def after_attribute_update_hook(mapper, connection, target):
    """
    Clear related cache after attribute updated
    """
    uuid = target.entity_uuid
    if uuid:
        entity = EntityModel()
        # This works because cache only cares about UUID
        # FIXME looks ugly
        entity.uuid = uuid
        entity.cache.clear()


class AttributeModel(_Jsonable, Model, metaclass=RichMixinMeta):
    """
    An attribute belong to only one entity
    Extra columns will be created to track the relation.
    """
    # TODO: Error on creation
    rmixin_registry = AttributeRegistry
    # If true, and uniq key will hava a extra constraint to make it unique in
    # the set of attributes belongs to a single entity
    __unique_attr__ = False
    # When given only create relationship with given entities or else will be a genetic attribute
    # Use require or namespace for entity
    __entities__ = None
    # Collector to use for relationship
    __collector__ = list
    # If specified will use associationproxy, and this is the key
    __outline__ = None
    # Used when outline is specified
    __creator__ = None
    # If cache the entry automatically after is't modified or created
    __autocache__ = False
    # If this is cacheable or not
    __cacheable__ = False

    entity_models = []

    @property
    def parent(self):
        return self.foreign_key

    @parent.setter
    def parent(self, parent):
        self.entity_uuid = parent

    def __repr__(self):
        return '<Metadash Attr of Enity "{}">'.format(self.entity_uuid)

    def as_dict(self, detail=False):
        dict_ = super(AttributeModel, self).as_dict()
        if detail:
            dict_['parent'] = self.parent
        return dict_

    @staticmethod
    def build_relationship(self):
        attribute = self
        entities = (
            [entity for entity in EntityRegistry.values()
             if attribute.ref_name not in entity.attribute_models.keys()]
        )
        for model in entities:
            model.attribute_models[attribute.ref_name] = attribute
            parentname = _get_alias_dict(model.__dict__)
            attribute.entity_models.append(parentname)

            # TODO: autocache = attribute.__autocache__
            cacheable = attribute.__cacheable__
            if cacheable:
                model.__cacheable_attributes__.add(attribute.ref_name)

            backref_name = attribute.__backref_name__
            proxy_name = attribute.__proxy_name__
            collector = attribute.__collector__
            outline = attribute.__outline__
            unique_attribute = attribute.__unique_attr__

            relationship = db.relationship(
                model,
                primaryjoin=foreign(attribute.entity_uuid) == remote(model.uuid),
                backref=backref(
                    backref_name, uselist=not unique_attribute,
                    collection_class=collector, cascade="all, delete-orphan"
                ),
                uselist=False, single_parent=True,
            )

            # will call _add_attribute of SQLAlchmey
            setattr(attribute, parentname, relationship)

            if outline:
                if hasattr(collector, '__proxy_args__'):
                    setattr(model, proxy_name,
                            association_proxy(backref_name, outline, **collector.__proxy_args__))
                else:
                    setattr(model, proxy_name,
                            association_proxy(backref_name, outline))

    def sub_init(baseclass, subclass, subclass_name, baseclasses, subclass_dict):
        # Clean cache
        subclass.build_relationship(subclass)

        on(subclass, 'after_update')(after_attribute_update_hook)
        on(subclass, 'after_insert')(after_attribute_update_hook)

    def sub_new(baseclass, subclass_name, baseclasses, subclass_dict):
        # pylint: disable=no-member

        table_args = subclass_dict.setdefault('__table_args__', ())
        outline = subclass_dict.setdefault('__outline__', None)

        tablename = _get_table_name_dict(subclass_dict)
        aliasname = _get_alias_dict(subclass_dict)

        proxy_name = subclass_dict.setdefault('__proxy_name__', pluralize(aliasname))
        backref_name = subclass_dict.setdefault('__backref_name__', "{}_ref".format(proxy_name))
        subclass_dict.setdefault('entity_models', AttributeModel.entity_models[:])

        subclass_dict['ref_name'] = proxy_name if outline else backref_name

        # Build foreign key and relationship
        has_primary_key = False
        for key, value in subclass_dict.items():
            if isinstance(value, db.Column):
                if value.unique_attribute:
                    table_args = table_args + (
                        db.UniqueConstraint('entity_uuid', key,
                                            name='_{}_metadash_attr_{}_uc'.format(
                                                tablename, value.name)), )
                if value.primary_key:
                    has_primary_key = True

        subclass_dict['entity_uuid'] = db.Column(
            UUID(), index=True, nullable=False, primary_key=not has_primary_key)
        table_args = table_args + (
            db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.index_uuid],
                                    name="_metadash_{}_fc".format(tablename),
                                    ondelete="CASCADE"),)
        subclass_dict['entity'] = db.relationship(
            MetadashEntity,
            primaryjoin=subclass_dict['entity_uuid'] == MetadashEntity.index_uuid,
            # backref=backref("attributes"), TODO
            uselist=False
        )

        # Apply changes
        subclass_dict['__table_args__'] = table_args


class SharedAttributeModel(_Jsonable, Model, metaclass=RichMixinMeta):
    """
    An attribute shared by multiple entity.
    A second table will be created to track the relation.
    """
    # TODO: Error on creation
    rmixin_registry = SharedAttributeRegistry
    # When given only create relationship with given entities or else will be a genetic attribute
    # Use require or namespace for entity
    __entities__ = None
    # Collector to use for relationship
    __collector__ = list
    # If specified will use associationproxy, and this is the key
    __outline__ = None  # TODO: Accept a dict
    # If cache the entry automatically after is't modified or created
    __autocache__ = False
    # If this is cacheable or not
    __cacheable__ = False

    entity_models = []

    parents = association_proxy(
        'entity',
        'uuid',
        creator=lambda uuid: MetadashEntity.query.filter(MetadashEntity.index_uuid == uuid).first()  # TODO: Error on empty query
    )

    def __repr__(self):
        return '<Metadash Shared Attr "{}">'.format(self.uuid)

    def as_dict(self, detail=False):
        dict_ = super(SharedAttributeModel, self).as_dict()
        if detail:
            dict_['parents'] = _format_for_json(self.parents)
        return dict_

    @staticmethod
    def build_relationship(self):
        attribute = self
        entities = (
            [entity for entity in EntityRegistry.values()
             if attribute.ref_name not in entity.attribute_models]
        )
        for model in entities:
            model.attribute_models[attribute.ref_name] = attribute
            parentname = _get_alias_dict(model.__dict__)
            attribute.entity_models.append(parentname)

            # TODO: autocache = attribute.__autocache__
            cacheable = attribute.__cacheable__
            if cacheable:
                model.__cacheable_attributes__.add(attribute.ref_name)

            backref_name = attribute.__backref_name__
            proxy_name = attribute.__proxy_name__
            collector = attribute.__collector__
            outline = attribute.__outline__

            relationship = db.relationship(
                model,
                secondary=attribute.__secondary__,
                primaryjoin=attribute.__secondary__.c.attr_uuid == attribute.uuid,
                secondaryjoin=foreign(attribute.__secondary__.c.entity_uuid) == remote(model.uuid),
                backref=backref(backref_name,
                                primaryjoin=attribute.__secondary__.c.entity_uuid == model.uuid,
                                secondaryjoin=foreign(attribute.__secondary__.c.attr_uuid) == remote(attribute.uuid), collection_class=collector),
                uselist=True,
                cascade="save-update, merge, refresh-expire, expunge",
            )

            setattr(attribute, parentname, relationship)

            if outline:
                if hasattr(collector, '__proxy_args__'):
                    creator = collector.__proxy_args__.get('creator', None)
                else:
                    creator = None

                def get_or_create_attribute(*args, **kwargs):
                    attribute_dict = {outline: args[0]}
                    attr = attribute.query.filter_by(**attribute_dict).first()
                    if not attr:
                        if creator:
                            attr = creator(*args, **kwargs)
                        else:
                            attr = attribute(*args, **kwargs)
                    return attr

                if hasattr(collector, '__proxy_args__'):
                    collector.__proxy_args__.set('creator', get_or_create_attribute)
                    setattr(model, proxy_name,
                            association_proxy(backref_name, outline, **collector.__proxy_args__))
                else:
                    setattr(model, proxy_name,
                            association_proxy(backref_name, outline, creator=get_or_create_attribute))

    def sub_init(baseclass, subclass, subclass_name, baseclasses, subclass_dict):
        subclass.build_relationship(subclass)

    def sub_new(mcs, classname, bases, dict_, **kwargs):
        # TODO: collector = dict_.setdefault('__collector__', list if not unique_attribute else None)
        outline = dict_.setdefault('__outline__', None)

        tablename = _get_table_name_dict(dict_)
        aliasname = _get_alias_dict(dict_)

        proxy_name = dict_.setdefault('__proxy_name__', pluralize(aliasname))
        backref_name = dict_.setdefault('__backref_name__', "{}_ref".format(proxy_name))
        dict_.setdefault('entity_models', SharedAttributeModel.entity_models[:])

        dict_['ref_name'] = proxy_name if outline else backref_name

        # Build foreign key and relationship
        has_primary_key = False
        for value in dict_.values():
            if isinstance(value, db.Column):
                if value.primary_key:
                    has_primary_key = True
                if value.unique_attribute:
                    value.unique = True
        dict_['uuid'] = db.Column(UUID(), index=True, nullable=False, unique=True,
                                  primary_key=not has_primary_key, default=uuid.uuid1)
        dict_['__secondary__'] = (
            db.Table("metadash_entities_{}".format(tablename),
                     db.Column('entity_uuid', UUID(), index=True),
                     db.Column('attr_uuid', UUID(), index=True),
                     db.ForeignKeyConstraint(
                         ['attr_uuid'], [dict_['uuid']], ondelete="CASCADE"),
                     db.ForeignKeyConstraint(
                         ['entity_uuid'], [MetadashEntity.index_uuid], ondelete="CASCADE")
                     )
        )
        dict_['entity'] = db.relationship(
            MetadashEntity,
            secondary=dict_['__secondary__'],
            primaryjoin=dict_['__secondary__'].c.attr_uuid == dict_['uuid'],
            secondaryjoin=dict_['__secondary__'].c.entity_uuid == MetadashEntity.index_uuid,
            # backref=backref("shared_attributes"), TODO
        )
