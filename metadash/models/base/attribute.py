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
from .utils import _pluralize, _get_model_name, _get_table_name_dict
from .utils import _all_leaf_class, _Jsonable, _format_for_json


Model = db.Model


class AttributeMeta(type(Model)):
    """
    Metaclass for defining new attribute class
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_):
        if classname == "AttributeModel":
            type.__new__(type, classname, bases, dict_)
            return

        super(AttributeMeta, cls).__init__(classname, bases, dict_)
        # TODO: Tidy up __init__ and __new__, remove radunant itrations
        for model in _all_leaf_class(EntityModel):
            model.attribute_models.append(cls)

    def __new__(mcs, classname, bases, dict_, **kwds):
        # pylint: disable=no-member
        if classname == "AttributeModel":
            return type.__new__(mcs, classname, bases, dict_)

        tablename = _get_table_name_dict(dict_)
        modelname = _get_model_name(dict_)
        table_args = dict_.get('__table_args__', ())
        unique_attribute = dict_.get('__unique_attr__', False) #TODO: Injection style
        entity_only = dict_.get('__entity_only__', []) #TODO: Injection style
        entity_models = AttributeModel.entity_models[:]

        backname = _pluralize(modelname) if not unique_attribute else modelname

        dict_['backname'] = backname
        dict_['entity_uuid'] = db.Column(UUID(), index=True, nullable=False, primary_key=True)

        table_args += (
            db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.uuid],
                                    name="_metadash_{}_f".format(tablename), ondelete="CASCADE"),
        )

        for key, value in dict_.items():
            if isinstance(value, db.Column) and value.unique_attribute:
                table_args = table_args + (
                    db.UniqueConstraint('entity_uuid', key,
                                        name='_{}_metadash_attr_{}_uc'.format(tablename, value.name))
                    , # Make it a tuple
                )

        for model in _all_leaf_class(EntityModel):
            if entity_only and model.__namespace__ not in entity_only:
                continue
            parentname = _get_model_name(model.__dict__)
            entity_models.append(parentname)
            dict_[parentname] = db.relationship(
                model,
                primaryjoin=foreign(dict_['entity_uuid']) == remote(model.uuid),
                backref=backref(
                    backname, uselist=not unique_attribute
                ),
                uselist=False, single_parent=True,
                cascade="all, delete-orphan",
            )

        dict_['entity'] = db.relationship(
            MetadashEntity,
            primaryjoin=dict_['entity_uuid'] == MetadashEntity.uuid,
            #backref=backref("attributes"), TODO
            uselist=False
        )

        dict_['__table_args__'] = table_args
        dict_['entity_models'] = entity_models

        return super(AttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwds)


class SharedAttributeMeta(type(Model)):
    """
    Metaclass for defining new attribute class
    """
    # pylint: disable=no-self-argument
    def __init__(cls, classname, bases, dict_):
        if classname != "SharedAttributeModel":
            super(SharedAttributeMeta, cls).__init__(classname, bases, dict_)
            for model in _all_leaf_class(EntityModel):
                model.attribute_models.append(cls)
        else:
            type.__new__(type, classname, bases, dict_)

    def __new__(mcs, classname, bases, dict_, **kwds):
        if classname == "SharedAttributeModel":
            return type.__new__(mcs, classname, bases, dict_)

        tablename = _get_table_name_dict(dict_)
        modelname = _get_model_name(dict_)
        backname = _pluralize(modelname)
        table_args = dict_.get('__table_args__', ())
        entity_only = dict_.get('__entity_only__', ())
        entity_models = AttributeModel.entity_models[:]

        # XXX: This looks more like another kind of entity...
        has_primary_key = False

        for value in dict_.values():
            if isinstance(value, db.Column):
                if value.primary_key:
                    has_primary_key = True
                if value.unique_attribute:
                    value.unique = True

        dict_['backname'] = backname
        dict_['uuid'] = db.Column(UUID(), index=True, nullable=False, unique=True,
                                  primary_key=(not has_primary_key), default=uuid.uuid1)

        dict_['__secondary__'] = (
            db.Table("metadash_entities_{}".format(tablename),
                     db.Column('entity_uuid', UUID(), index=True),
                     db.Column('attr_uuid', UUID(), index=True),
                     db.ForeignKeyConstraint(['attr_uuid'], [dict_['uuid']], ondelete="CASCADE"),
                     db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.uuid], ondelete="CASCADE")
                    )
        )

        for model in _all_leaf_class(EntityModel):
            if entity_only and model.__namespace__ not in entity_only:
                continue
            parentname = _get_model_name(model.__dict__)
            parentsname = _pluralize(parentname)
            entity_models.append(parentsname)
            dict_[parentsname] = db.relationship(
                model,
                secondary=dict_['__secondary__'],
                primaryjoin=dict_['__secondary__'].c.attr_uuid == dict_['uuid'],
                secondaryjoin=foreign(dict_['__secondary__'].c.entity_uuid) == remote(model.uuid),
                backref=backref(backname,
                                primaryjoin=dict_['__secondary__'].c.entity_uuid == model.uuid,
                                secondaryjoin=foreign(dict_['__secondary__'].c.attr_uuid) == remote(dict_['uuid'])),
                uselist=True,
                cascade="save-update, merge, refresh-expire, expunge",
            )

        dict_['entity'] = db.relationship(
            MetadashEntity,
            secondary=dict_['__secondary__'],
            primaryjoin=dict_['__secondary__'].c.attr_uuid == dict_['uuid'],
            secondaryjoin=dict_['__secondary__'].c.entity_uuid == MetadashEntity.uuid,
            #backref=backref("shared_attributes"), TODO
        )

        dict_['__table_args__'] = table_args
        dict_['entity_models'] = entity_models

        return super(SharedAttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwds)


class AttributeModel(_Jsonable, Model, metaclass=AttributeMeta):
    """
    An attribute belong to only one entity
    Extra columns will be created to track the relation.
    """
    #TODO: Error on creation

    __entity_only__ = None

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
    #TODO: Error on creation

    __entity_only__ = None

    entity_models = []

    parents = association_proxy(
        'entity',
        'uuid',
        creator=lambda uuid: MetadashEntity.query.filter(MetadashEntity.uuid == uuid).first() #TODO: Error on empty query
    )

    def __repr__(self):
        return '<Metadash Shared Attr "{}">'.format(self.uuid)

    def as_dict(self, detail=False):
        dict_ = super(SharedAttributeModel, self).as_dict()
        if detail:
            dict_['parents'] = _format_for_json(self.parents)
        return dict_
