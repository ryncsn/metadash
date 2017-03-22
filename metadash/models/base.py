"""
Helper to define EAV style models.

Considering:
* have growing entity and entity types, and needs flexable attributes,
* may need to add / delete a kind of attri and related code.
* may need to split some part the database out into another component.

To make it easier to index entities cross app / db / table, use uuid as
key of diffrent type of entities.
Use a namespace uuid (NS) to distinguish between different type of entities.

And to make the integrity easier, split out all the key (NS and UUID) of
diffrent entities into one big table, which also make it more cache friendly.
"""
import uuid

from sqlalchemy import join
from sqlalchemy import event
from sqlalchemy.orm import backref, foreign, remote
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.associationproxy import association_proxy

from metadash.models import db, UUID, get_or_create, get
from metadash import logger

Model = db.Model

URN = '123e4567-e89b-12d3-a456-426655440000'


def _extend_column_arg_patch():
    """
    Monkey patch for some custom kwargs.
    """
    from sqlalchemy.sql.schema import Column

    _origin_column_init = Column.__init__

    def _extend_attr(self, *args, **kwargs):
        self.unique_attribute = kwargs.pop('unique_attribute', False)
        _origin_column_init(self, *args, **kwargs)

    Column.__init__ = _extend_attr

_extend_column_arg_patch()


def _all_leaf(cls):
    subs = cls.__subclasses__()
    return sum([_all_leaf(cls) for cls in subs], []) if subs else [cls]


def _all_leaf_class(cls):
    if cls.__subclasses__():
        return _all_leaf(cls)
    return []


def _get_table_name_dict(dict_):
    _tablename = dict_.get('__tablename__', None)
    _table = dict_.get('__table__', None)
    tablename = _tablename or _table.name
    assert(tablename and isinstance(tablename, (str)))
    return tablename


def _get_model_name(dict_):
    _alias = dict_.get('__alias__', None)
    _tablename = _get_table_name_dict(dict_)
    modelname = _alias or _tablename
    assert(modelname and isinstance(modelname, (str)))
    return modelname


def _pluralize(singular):
    # FIXME: it's wrong, totally
    if singular.endswith('y'):
        return "{}s".format(singular[:-1])
    return "{}s".format(singular) if not singular.endswith('s') else singular #FIXME


def _format_for_json(data):
    if hasattr(data, 'as_dict'):
        return data.as_dict()
    elif isinstance(data, (int, float, str)):
        return data
    elif isinstance(data, dict):
        return dict([(k, _format_for_json(v)) for k, v in data.items()])
    elif hasattr(data, '__iter__'):
        return [_format_for_json(_value) for _value in data]
    else:
        return str(data)


class MetadashEntity(Model):
    """
    The table indexing all NS and UUID of all type of entities.

    NS: Used to identify which plugin/model a entity belongs to.
    UUID: Unique identifier
    """
    __tablename__ = "metadash_entity"
    __table_args__ = (
        db.UniqueConstraint('namespace', 'uuid', name='_metadash_entity_uc'),
    )
    __namespace_map__ = {}

    namespace = db.Column(UUID(), index=True, nullable=False, primary_key=True)
    uuid = db.Column(UUID(), index=True, nullable=False, unique=True, primary_key=True)

    def cast(self):
        pass #TODO: cast into the right instance according to namespace


MetadashEntity.__namespace_map__[
    uuid.uuid5(uuid.UUID(URN), MetadashEntity.__tablename__)] = MetadashEntity


class _Jsonable(object):
    # pylint: disable=no-member
    def as_dict(self, only=None, exclude=None, extra=None):
        """
        Format a model instance into json.
        """
        return dict([(_c.name, _format_for_json(getattr(self, _c.name)))
                     for _c in
                     only or set(self.__table__.columns + (extra or [])) - set(exclude or [])])


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

        # pylint: disable=no-member
        # FIXME: this might be wrong
        def _before_insert(mapper, connection, target):
            target.uuid = target.uuid if target.uuid is not None else uuid.uuid4()
            connection.execute(
                MetadashEntity.__table__.insert(),
                {
                    "namespace": target.namespace,
                    "uuid": target.uuid
                },
            )

        def _after_delete(mapper, connection, target):
            connection.execute(
                MetadashEntity.__table__.delete().where(
                    MetadashEntity.__table__.c.uuid == target.uuid
                ),
            ),

        event.listen(cls, 'before_insert', _before_insert)
        event.listen(cls, 'after_delete', _after_delete)

        MetadashEntity.__namespace_map__[cls.namespace] = cls

    def __new__(mcs, classname, bases, dict_):
        if classname == 'EntityModel':
            return type.__new__(mcs, classname, bases, dict_)

        dict_ = dict(dict_) # Make it writable

        namespace = dict_.get('namespace',
                              uuid.uuid5(uuid.UUID(URN), _get_table_name_dict(dict_)))
        assert isinstance(namespace, uuid.UUID)

        dict_['uuid'] = db.Column(
            UUID(), db.ForeignKey(MetadashEntity.uuid, ondelete="CASCADE", onupdate="RESTRICT"),
            index=True, nullable=False, primary_key=True, default=uuid.uuid4,
        )
        dict_['namespace'] = namespace
        dict_['attribute_models'] = EntityModel.attribute_models[:]

        return super(EntityMeta, mcs).__new__(mcs, classname, bases, dict_)


class EntityModel(_Jsonable, db.Model, metaclass=EntityMeta):
    """
    Entity Model base that provide support for convinient
    attribute access.

    namespace is hardcodes in each EntityModel and generated with
    uuid5(NS=URN, <tablename>) if not privided.

    Use hardcoded NS, each table have a NS.
    """

    __alias__ = None

    attribute_models = []

    def identity(self):
        return '{}:{}'.format(self.namespace, self.uuid)

    def as_dict(self, detail=False):
        dict_ = super(EntityModel, self).as_dict()
        if detail:
            for model in self.attribute_models:
                dict_[model.backname] = _format_for_json(getattr(self, model.backname))
        return dict_


class AttributeMeta(type(db.Model)):
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
        backname = _pluralize(modelname)
        table_args = dict_.get('__table_args__', ())
        entity_only = dict_.get('__entity_only__', [])
        entity_models = AttributeModel.entity_models[:]

        dict_['backname'] = backname
        dict_['foreign_uuid'] = db.Column(UUID(), index=True, nullable=False, primary_key=True)

        table_args += (
            db.ForeignKeyConstraint(['foreign_uuid'], [MetadashEntity.uuid],
                                    name="_metadash_{}_f".format(tablename), ondelete="CASCADE"),
        )

        for key, value in dict_.items():
            if isinstance(value, db.Column) and value.unique_attribute:
                table_args = table_args + (
                    db.UniqueConstraint('foreign_uuid', key,
                                        name='_{}_metadash_attr_{}_uc'.format(tablename, value.name))
                    , # Make it a tuple
                )

        for model in _all_leaf_class(EntityModel):
            if entity_only and model.namespace not in entity_only:
                continue
            parentname = _get_model_name(model.__dict__)
            entity_models.append(parentname)
            dict_[parentname] = db.relationship(
                model,
                primaryjoin=foreign(dict_['foreign_uuid']) == remote(model.uuid),
                backref=backref(
                    backname, uselist=True
                ),
                uselist=False, single_parent=True,
                cascade="all, delete-orphan",
            )

        dict_['entity'] = db.relationship(
            MetadashEntity,
            primaryjoin=dict_['foreign_uuid'] == MetadashEntity.uuid,
            #backref=backref("attributes"), TODO
            uselist=False
        )

        dict_['__table_args__'] = table_args
        dict_['entity_models'] = entity_models

        return super(AttributeMeta, mcs).__new__(mcs, classname, bases, dict_, **kwds)


class SharedAttributeMeta(type(db.Model)):
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
                                  primary_key=(not has_primary_key), default=uuid.uuid4)

        dict_['__secondary__'] = (
            db.Table("metadash_entities_{}".format(tablename),
                     db.Column('entity_uuid', UUID(), index=True),
                     db.Column('attr_uuid', UUID(), index=True),
                     db.ForeignKeyConstraint(['attr_uuid'], [dict_['uuid']], ondelete="CASCADE"),
                     db.ForeignKeyConstraint(['entity_uuid'], [MetadashEntity.uuid], ondelete="CASCADE")
                    )
        )

        for model in _all_leaf_class(EntityModel):
            if entity_only and model.namespace not in entity_only:
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


class AttributeModel(_Jsonable, db.Model, metaclass=AttributeMeta):
    """
    An attribute belong to only one entity
    Extra columns will be created to track the relation.
    """

    __entity_only__ = None

    entity_models = []

    @property
    def parent(self):
        return self.foreign_key

    @parent.setter
    def parent(self, parent):
        self.foreign_uuid = parent

    def __repr__(self):
        return '<Metadash Attr of Enity "{}">'.format(self.foreign_uuid)

    def as_dict(self, detail=False):
        dict_ = super(AttributeModel, self).as_dict()
        if detail:
            dict_['parent'] = self.parent
        return dict_


class SharedAttributeModel(_Jsonable, db.Model, metaclass=SharedAttributeMeta):
    """
    An attribute shared by multiple entity.
    A second table will be created to track the relation.
    """

    __entity_only__ = None

    entity_models = []

    parents = association_proxy(
        'entity',
        'uuid',
        creator=lambda uuid: MetadashEntity.query.filter(MetadashEntity.uuid == uuid).first()
    )

    def __repr__(self):
        return '<Metadash Shared Attr "{}">'.format(self.uuid)

    def as_dict(self, detail=False):
        dict_ = super(SharedAttributeModel, self).as_dict()
        if detail:
            dict_['parents'] = _format_for_json(self.parents)
        return dict_


def relation(*args, **kwargs):
    #TODO: Helper to create relation
    return db.relation(*args, **kwargs)
