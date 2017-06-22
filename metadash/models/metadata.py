"""
Some basic metadata
"""
from sqlalchemy.orm.collections import attribute_mapped_collection
from .base import SharedAttributeModel, AttributeModel
from . import db


class Property(AttributeModel):
    """
    Property, key-value pair, indexed for querying
    Object <-- Property
    """
    __alias__ = 'property'
    __tablename__ = 'metadash_property'
    __collector__ = attribute_mapped_collection("key")
    __composer__ = "value"

    key = db.Column(db.String(255), nullable=False, index=True, primary_key=True, unique_attribute=True)
    value = db.Column(db.String(3072), nullable=False, index=True)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Property "{}":"{}" of Entiry({}): %s, %s:%s>'.format(self.key, self.value, self.entity)


def list_property_creator(key, value):
    if not isinstance(value, list):
        return Property(key, value)
    else:
        if len(value) > 1 or len(value) == 0:
            raise NotImplementedError()
        return [Property(key, value) for value in value]


Property.__creator__ = list_property_creator


class Detail(AttributeModel):
    """
    Detail, key-value pair with big value, for logs, huge parameters.
    Only key is indexed.
    Object <-- Detail
    """
    __alias__ = 'detail'
    __tablename__ = 'metadash_detail'
    __collector__ = attribute_mapped_collection("key")
    __composer__ = "value"

    key = db.Column(db.String(255), nullable=False, index=True, primary_key=True, unique_attribute=True)
    value = db.Column(db.Text(), nullable=False)

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
    __collector__ = set
    __composer__ = "name"

    name = db.Column(db.String(255), nullable=False, index=True, unique_attribute=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag "{}" of Entity({}): %s, %s:%s>'.format(self.name, self.entity)
