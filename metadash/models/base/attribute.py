"""
Helper to define attribute/metadata models.
"""
import uuid

from sqlalchemy.orm import backref, foreign, remote
from sqlalchemy.ext.associationproxy import association_proxy

from ..types import UUID
from .. import db

from metadash.event import on
from .entity import MetadashEntity, EntityModel
from .utils import _pluralize, _get_alias_dict, _get_table_name_dict
from .utils import _all_leaf_class, _Jsonable, _format_for_json


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


Model = db.Model


def _find_entity(key):
    if isinstance(key, EntityModel):
        return key
    elif isinstance(key, (str)):
        # TODO: Poor Performance
        for model in _all_leaf_class(EntityModel):
            if model.__name__ == key:
                return model
            if getattr(model, '__namespace__') == key:
                return model
            if getattr(model, '__table__') == key:
                return model
    raise RuntimeError()


class AttributeMeta(type(Model)):
    """
    Metaclass for defining new attribute class
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_, **kwargs):
        if classname == "AttributeModel":
            type.__init__(type, classname, bases, dict_, **kwargs)
        else:
            super(AttributeMeta, cls).__init__(classname, bases, dict_)

        # Clean cache
        on(cls, 'after_update')(after_attribute_update_hook)
        on(cls, 'after_insert')(after_attribute_update_hook)

    def __new__(mcs, classname, bases, dict_, **kwargs):
        # pylint: disable=no-member
        if classname == "AttributeModel":
            return type.__new__(mcs, classname, bases, dict_, **kwargs)

        # Default values
        unique_attribute = dict_.setdefault('__unique_attr__', False)

        autocache = dict_.setdefault('__autocache__', False)
        cacheable = dict_.setdefault('__cacheable__', False)
        table_args = dict_.setdefault('__table_args__', ())
        entities_only = dict_.setdefault('__entities__', None)
        collector = dict_.setdefault('__collector__', list if not unique_attribute else None)
        outline = dict_.setdefault('__outline__', None)
        creator = dict_.setdefault('__creator__', None)

        tablename = _get_table_name_dict(dict_)
        aliasname = _get_alias_dict(dict_)

        proxy_name = dict_.setdefault('__proxy_name__', _pluralize(aliasname))
        backref_name = dict_.setdefault('__backref_name__', "{}_ref".format(proxy_name))
        entity_models = dict_.setdefault('entity_models',
                                         AttributeModel.entity_models[:])

        dict_['ref_name'] = proxy_name if outline else backref_name

        # Build foreign key and relationship
        has_primary_key = False
        for key, value in dict_.items():
            if isinstance(value, db.Column):
                if value.unique_attribute:
                    table_args = table_args + (
                        db.UniqueConstraint('entity_uuid', key,
                                            name='_{}_metadash_attr_{}_uc'.format(
                                                tablename, value.name)), )
                if value.primary_key:
                    has_primary_key = True

        dict_['entity_uuid'] = db.Column(
            UUID(), index=True, nullable=False, primary_key=not has_primary_key)
        table_args = table_args + (
            db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.index_uuid],
                                    name="_metadash_{}_fc".format(tablename),
                                    ondelete="CASCADE"),)
        dict_['entity'] = db.relationship(
            MetadashEntity,
            primaryjoin=dict_['entity_uuid'] == MetadashEntity.index_uuid,
            # backref=backref("attributes"), TODO
            uselist=False
        )

        # Apply changes
        dict_['__table_args__'] = table_args

        return super(AttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwargs)


class SharedAttributeMeta(type(Model)):
    """
    Metaclass for defining new attribute class
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_, **kwargs):
        if classname == "SharedAttributeModel":
            type.__init__(type, classname, bases, dict_, **kwargs)
        else:
            super(SharedAttributeMeta, cls).__init__(classname, bases, dict_, **kwargs)

    def __new__(mcs, classname, bases, dict_, **kwargs):
        # XXX: This looks more like another kind of entity...
        if classname == "SharedAttributeModel":
            return type.__new__(mcs, classname, bases, dict_)

        # TODO: Injection style
        # Default values
        autocache = dict_.setdefault('__autocache__', False)
        cacheable = dict_.setdefault('__cacheable__', False)
        table_args = dict_.setdefault('__table_args__', ())
        entities_only = dict_.setdefault('__entities__', None)
        collector = dict_.setdefault('__collector__', list)
        # TODO: collector = dict_.setdefault('__collector__', list if not unique_attribute else None)
        outline = dict_.setdefault('__outline__', None)
        creator = dict_.setdefault('__creator__', None)

        tablename = _get_table_name_dict(dict_)
        aliasname = _get_alias_dict(dict_)

        proxy_name = dict_.setdefault('__proxy_name__', _pluralize(aliasname))
        backref_name = dict_.setdefault('__backref_name__', "{}_ref".format(proxy_name))
        entity_models = dict_.setdefault('entity_models',
                                         SharedAttributeModel.entity_models[:])

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

        return super(SharedAttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwargs)


class AttributeModel(_Jsonable, Model, metaclass=AttributeMeta):
    """
    An attribute belong to only one entity
    Extra columns will be created to track the relation.
    """
    # TODO: Error on creation
    # If true, and uniq key will hava a extra constraint to make it unique in
    # the set of attributes belongs to a single entity
    __unique_attr__ = False
    # When given only create relationship with given entities or else will be a genetic attribute
    # Use require or namespace for entity
    __entities__ = None
    # Collector to use for relationship
    __collector__ = list
    # If specified will use associationproxy, and this is the key
    __outline__ = None  # TODO: Accept a dict
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


class SharedAttributeModel(_Jsonable, Model, metaclass=SharedAttributeMeta):
    """
    An attribute shared by multiple entity.
    A second table will be created to track the relation.
    """
    # TODO: Error on creation
    # When given only create relationship with given entities or else will be a genetic attribute
    # Use require or namespace for entity
    __entities__ = None
    # Collector to use for relationship
    __collector__ = list
    # If specified will use associationproxy, and this is the key
    __outline__ = None  # TODO: Accept a dict
    # Used when outline is specified
    __creator__ = None
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


def init_attribute(attribute):
    # TODO: DRY
    if hasattr(attribute, '__md_initialized'):
        return
    setattr(attribute, '__md_initialized', True)

    entities = (
        [_find_entity(e) for e in attribute.__entities__]
        if attribute.__entities__ is not None else _all_leaf_class(EntityModel)
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
        creator = attribute.__creator__
        unique_attribute = attribute.__unique_attr__

        setattr(attribute, parentname, db.relationship(
            model,
            primaryjoin=foreign(attribute.entity_uuid) == remote(model.uuid),
            backref=backref(
                backref_name, uselist=not unique_attribute, collection_class=collector
            ),
            uselist=False, single_parent=True,
            cascade="all, delete-orphan",
        ))

        if outline:
            setattr(model, proxy_name,
                    association_proxy(backref_name, outline,
                                      **({'creator': lambda *args, **kwargs: attribute.__creator__(*args, **kwargs)}
                                         if creator else {})))


def init_shared_attribute(attribute):
    if hasattr(attribute, '__md_initialized'):
        return
    setattr(attribute, '__md_initialized', True)

    entities = (
        [_find_entity(e) for e in attribute.__entities__]
        if attribute.__entities__ is not None else _all_leaf_class(EntityModel)
    )
    for model in entities:
        model.attribute_models[attribute.ref_name] = attribute
        parentname = _get_alias_dict(model.__dict__)
        parentsname = _pluralize(parentname)
        attribute.entity_models.append(parentname)

        # TODO: autocache = attribute.__autocache__
        cacheable = attribute.__cacheable__
        if cacheable:
            model.__cacheable_attributes__.add(attribute.ref_name)

        backref_name = attribute.__backref_name__
        proxy_name = attribute.__proxy_name__
        collector = attribute.__collector__
        outline = attribute.__outline__
        creator = attribute.__creator__

        setattr(attribute, parentsname, db.relationship(
            model,
            secondary=attribute.__secondary__,
            primaryjoin=attribute.__secondary__.c.attr_uuid == attribute.uuid,
            secondaryjoin=foreign(attribute.__secondary__.c.entity_uuid) == remote(model.uuid),
            backref=backref(backref_name,
                            primaryjoin=attribute.__secondary__.c.entity_uuid == model.uuid,
                            secondaryjoin=foreign(attribute.__secondary__.c.attr_uuid) == remote(attribute.uuid), collection_class=collector),
            uselist=True,
            cascade="save-update, merge, refresh-expire, expunge",
        ))

        if outline:
            def get_or_create_attribute(*args, **kwargs):
                attribute_dict = {outline: args[0]}
                attr = attribute.query.filter_by(**attribute_dict).first()
                if not attr:
                    if creator:
                        attr = creator(*args, **kwargs)
                    else:
                        attr = attribute(*args, **kwargs)
                return attr

            setattr(model, proxy_name,
                    association_proxy(backref_name, outline, creator=get_or_create_attribute))


def init():
    """
    Build relationship
    """
    for attribute in _all_leaf_class(AttributeModel):
        init_attribute(attribute)
    for attribute in _all_leaf_class(SharedAttributeModel):
        init_shared_attribute(attribute)
