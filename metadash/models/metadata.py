"""
Some basic metadata
"""
from sqlalchemy.orm.collections import attribute_mapped_collection
from .base import SharedAttributeModel, AttributeModel
from .collections import attribute_mapped_list_collection
from . import db


class Property(AttributeModel):
    """
    Property, key-value pairs, indexed for querying
    Object <-- Property
    """
    __alias__ = 'property'
    __tablename__ = 'metadash_property'
    __collector__ = attribute_mapped_list_collection("key")
    __outline__ = "value"
    __cacheable__ = True

    # Use a standalone id, a surrogate key to allow a entity to have multiple
    # property with same 'key' value
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)

    key = db.Column(db.String(255), nullable=False, index=True)
    value = db.Column(db.String(3072), nullable=True, index=True)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Property "{}":"{}" of Entiry({}): %s, %s:%s>'.format(self.key, self.value, self.entity)

    @staticmethod
    def all_values(entity_model, key, limit=None):
        """
        Get all candidate value of properties belongs to a entity model
        """
        q = db.session.query(Property.value)\
            .select_from(entity_model).join(Property)\
            .filter(Property.key == key)\
            .distinct().limit(limit or 50)
        return [r.value for r in q.all()]


def list_property_creator(key, value):
    if not isinstance(value, list):
        return Property(key, value)
    else:
        return [Property(key, value) for value in value]


Property.__creator__ = list_property_creator


class Detail(AttributeModel):
    """
    """
    __alias__ = 'detail'
    __tablename__ = 'metadash_detail'
    __collector__ = attribute_mapped_collection("key")
    __outline__ = "value"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), nullable=False, index=True, unique_attribute=True)
    value = db.Column(db.Text(), nullable=True)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Detail "{}":"{}" of Entiry({}): %s, %s:%s>'.format(self.key, self.value, self.entity)


class Tag(SharedAttributeModel):
    """
    Entity --- Tag
    """
    __alias__ = 'tag'
    __tablename__ = 'metadash_tag'
    __collector__ = list
    __outline__ = 'name'
    __cacheable__ = True

    name = db.Column(db.String(255), nullable=False, index=True, unique_attribute=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag "{}" of Entity({}): %s, %s:%s>'.format(self.name, self.entity)

    @staticmethod
    def all_tags(entity_model, limit=None):
        """
        Get all candidate tags belongs to a entity model
        """
        q = db.session.query(Tag.name)\
            .select_from(entity_model).join(Tag.__secondary__).join(Tag)\
            .distinct().limit(limit or 50)
        return [r.name for r in q.all()]
