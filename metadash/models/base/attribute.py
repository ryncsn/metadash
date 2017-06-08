"""
Helper to define attribute/metadata models.
"""
import uuid

from sqlalchemy.orm import backref, foreign, remote
from sqlalchemy.ext.associationproxy import association_proxy

from ..types import UUID
from .. import db
from ... import logger

from .entity import MetadashEntity, EntityModel
from .utils import _pluralize, _get_alias_dict, _get_table_name_dict
from .utils import _all_leaf_class, _Jsonable, _format_for_json


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
            return

        super(AttributeMeta, cls).__init__(classname, bases, dict_)
        # TODO: Tidy up __init__ and __new__, remove radunant itrations
        for model in _all_leaf_class(EntityModel):
            model.attribute_models.append(cls)

    def __new__(mcs, classname, bases, dict_, **kwargs):
        # pylint: disable=no-member
        if classname == "AttributeModel":
            return type.__new__(mcs, classname, bases, dict_, **kwargs)

        tablename = _get_table_name_dict(dict_)
        aliasname = _get_alias_dict(dict_)
        # TODO: Injection style
        table_args = dict_.get('__table_args__', ())
        entities_only = dict_.get('__entities__', [])
        unique_attribute = dict_.get('__unique_attr__', False)
        collector = dict_.get('__collector__', list)
        composer = dict_.get('__composer__', None)
        creator = dict_.get('__creator__', None)

        entities = [_find_entity(e) for e in entities_only] or _all_leaf_class(EntityModel)

        proxy_name = _pluralize(aliasname) if not unique_attribute else aliasname
        backref_name = "{}_ref".format(proxy_name)
        entity_models = AttributeModel.entity_models[:]

        dict_['key_name'] = proxy_name if composer else backref_name
        dict_['entity_uuid'] = db.Column(
            UUID(), index=True, nullable=False, primary_key=True)
        table_args += (
            db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.uuid],
                                    name="_metadash_{}_fc".format(tablename),
                                    ondelete="CASCADE"),)

        for key, value in dict_.items():
            if isinstance(value, db.Column) and value.unique_attribute:
                table_args = table_args + (
                    db.UniqueConstraint('entity_uuid', key,
                                        name='_{}_metadash_attr_{}_uc'.format(
                                            tablename, value.name)), )

        for model in entities:
            parentname = _get_alias_dict(model.__dict__)
            entity_models.append(parentname)
            dict_[parentname] = db.relationship(
                model,
                primaryjoin=foreign(dict_['entity_uuid']) == remote(model.uuid),
                backref=backref(
                    backref_name, uselist=not unique_attribute, collection_class=collector
                ),
                uselist=False, single_parent=True,
                cascade="all, delete-orphan",
            )
            if composer:
                setattr(model, proxy_name, association_proxy(backref_name, composer),
                        **({'creator': creator} if creator else {}))

        dict_['entity'] = db.relationship(
            MetadashEntity,
            primaryjoin=dict_['entity_uuid'] == MetadashEntity.uuid,
            # backref=backref("attributes"), TODO
            uselist=False
        )

        dict_['__table_args__'] = table_args
        dict_['entity_models'] = entity_models

        return super(AttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwargs)


class SharedAttributeMeta(type(Model)):
    """
    Metaclass for defining new attribute class
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_, **kwargs):
        if classname != "SharedAttributeModel":
            super(SharedAttributeMeta, cls).__init__(classname, bases, dict_, **kwargs)
            for model in _all_leaf_class(EntityModel):
                model.attribute_models.append(cls)
        else:
            type.__init__(type, classname, bases, dict_, **kwargs, **kwargs)

    def __new__(mcs, classname, bases, dict_, **kwargs):
        # XXX: This looks more like another kind of entity...
        if classname == "SharedAttributeModel":
            return type.__new__(mcs, classname, bases, dict_)

        tablename = _get_table_name_dict(dict_)
        aliasname = _get_alias_dict(dict_)
        # TODO: Injection style
        table_args = dict_.get('__table_args__', ())
        entities_only = dict_.get('__entities__', [])
        collector = dict_.get('__collector__', list)
        composer = dict_.get('__composer__', None)
        creator = dict_.get('__creator__', None)

        entities = [_find_entity(e) for e in entities_only] or _all_leaf_class(EntityModel)

        proxy_name = _pluralize(aliasname)
        backref_name = "{}_ref".format(proxy_name)
        entity_models = AttributeModel.entity_models[:]

        has_primary_key = False
        for value in dict_.values():
            if isinstance(value, db.Column):
                if value.primary_key:
                    has_primary_key = True
                if value.unique_attribute:
                    value.unique = True

        dict_['key_name'] = proxy_name if composer else backref_name
        dict_['uuid'] = db.Column(UUID(), index=True, nullable=False, unique=True,
                                  primary_key=not has_primary_key, default=uuid.uuid1)

        dict_['__secondary__'] = (
            db.Table("metadash_entities_{}".format(tablename),
                     db.Column('entity_uuid', UUID(), index=True),
                     db.Column('attr_uuid', UUID(), index=True),
                     db.ForeignKeyConstraint(
                         ['attr_uuid'], [dict_['uuid']], ondelete="CASCADE"),
                     db.ForeignKeyConstraint(
                         ['entity_uuid'], [MetadashEntity.uuid], ondelete="CASCADE")
                     )
        )

        for model in entities:
            parentname = _get_alias_dict(model.__dict__)
            parentsname = _pluralize(parentname)
            entity_models.append(parentsname)
            dict_[parentsname] = db.relationship(
                model,
                secondary=dict_['__secondary__'],
                primaryjoin=dict_['__secondary__'].c.attr_uuid == dict_['uuid'],
                secondaryjoin=foreign(dict_['__secondary__'].c.entity_uuid) == remote(model.uuid),
                backref=backref(backref_name,
                                primaryjoin=dict_['__secondary__'].c.entity_uuid == model.uuid,
                                secondaryjoin=foreign(dict_['__secondary__'].c.attr_uuid) == remote(dict_['uuid']), collection_class=collector),
                uselist=True,
                cascade="save-update, merge, refresh-expire, expunge",
            )

            if composer:
                setattr(model, proxy_name,
                        association_proxy(backref_name, composer,
                                          **({'creator': creator} if creator else {})))

        dict_['entity'] = db.relationship(
            MetadashEntity,
            secondary=dict_['__secondary__'],
            primaryjoin=dict_['__secondary__'].c.attr_uuid == dict_['uuid'],
            secondaryjoin=dict_['__secondary__'].c.entity_uuid == MetadashEntity.uuid,
            # backref=backref("shared_attributes"), TODO
        )

        dict_['__table_args__'] = table_args
        dict_['entity_models'] = entity_models

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
    __composer__ = None  # TODO: Accept a dict
    # Used when composer is specified
    __creator__ = None

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
    __composer__ = None  # TODO: Accept a dict
    # Used when composer is specified
    __creator__ = None

    entity_models = []

    parents = association_proxy(
        'entity',
        'uuid',
        creator=lambda uuid: MetadashEntity.query.filter(MetadashEntity.uuid == uuid).first()  # TODO: Error on empty query
    )

    def __repr__(self):
        return '<Metadash Shared Attr "{}">'.format(self.uuid)

    def as_dict(self, detail=False):
        dict_ = super(SharedAttributeModel, self).as_dict()
        if detail:
            dict_['parents'] = _format_for_json(self.parents)
        return dict_
