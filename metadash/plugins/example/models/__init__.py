"""
Example Plugin, also used for testing and debug
"""
from metadash.models.base import EntityModel
from metadash.models.service import provide
from metadash import db


@provide('example')
class ExampleEntity(EntityModel):  # Inherit from EntityModel, so have a UUID
    """
    Example Entity
    """
    __tablename__ = __alias__ = __namespace__ = 'example'
    name = db.Column(db.String(32), primary_key=True)
