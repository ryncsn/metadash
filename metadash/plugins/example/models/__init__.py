"""
Example Plugin, also used for testing and debug
"""
import time

from metadash.models.base import EntityModel
from metadash.injector import provide
from metadash.cache import cache_on_entity, cached_entity_property
from metadash import db


@provide('example')
class ExampleEntity(EntityModel):  # Inherit from EntityModel, so have a UUID
    """
    Example Entity
    """
    __tablename__ = __alias__ = __namespace__ = 'example'
    name = db.Column(db.String(32), primary_key=True, nullable=False)

    @cache_on_entity()
    def cached_function(self):
        return 'Cached Function'

    @cached_entity_property()
    def cached_property(self):
        time.sleep(1)
        return 'Cached Property'
