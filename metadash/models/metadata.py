"""
Some basic metadata
"""
from metadash.models.base import SharedAttributeModel, AttributeModel
from metadash.models import db


class Property(AttributeModel):
    """
    Property, key-value pair, indexed for querying
    Object <-- Property
    """
    __alias__ = 'property'
    __tablename__ = 'metadash_property'

    key = db.Column(db.String(255), nullable=False, index=True, primary_key=True, unique_attribute=True)
    value = db.Column(db.String(3072), nullable=False, index=True)

    def __repr__(self):
        return '<Property "{}":"{}" of Entiry({}): %s, %s:%s>'.format(self.key, self.value, self.entity)


class Detail(AttributeModel):
    """
    Detail, key-value pair with big value, for logs, huge parameters.
    Only key is indexed.
    Object <-- Detail
    """
    __alias__ = 'detail'
    __tablename__ = 'metadash_detail'

    key = db.Column(db.String(255), nullable=False, index=True, primary_key=True, unique_attribute=True)
    value = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Detail "{}":"{}" of Entiry({}): %s, %s:%s>'.format(self.key, self.value, self.entity)


class Tag(SharedAttributeModel):
    """
    Entity --- Tag
    """
    __alias__ = 'tag'
    __tablename__ = 'metadash_tag'

    name = db.Column(db.String(255), nullable=False, index=True, unique_attribute=True)

    def __repr__(self):
        return '<Tag "{}" of Entity({}): %s, %s:%s>'.format(self.name, self.entity)
