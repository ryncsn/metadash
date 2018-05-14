"""
Basic test boilerplate
"""
import uuid

from metadash.test.api import BasicTestCase
from metadash.cache import (
    cached_property, cached_entity_property,
    cache_on_entity, cache_on_entity_model)
from metadash.models import db
from metadash.models.base import EntityModel


class TestObject(object):
    @cached_property
    def test_cached_prop(self, dummy_value=None):
        return str(uuid.uuid1())


class Entity(EntityModel):  # pragma: no cover
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'metadash-cache-test'

    value = db.Column(db.String())

    @cache_on_entity()
    def test_cached_model_value(self, dummy_value=None):
        return str(uuid.uuid1())

    @cache_on_entity_model()
    def test_cached_fn(self, dummy_value=None):
        return str(uuid.uuid1())

    @cached_entity_property()
    def test_cached_prop(self):
        return str(uuid.uuid1())

    def __init__(self, value):
        self.value = value


class EntityTest(BasicTestCase):  # pragma: no cover
    def test_cache_property(self):
        obj = TestObject()
        first_call = obj.test_cached_prop
        second_call = obj.test_cached_prop

        self.assertEqual(first_call, second_call)

    def test_instance_cache_get(self):
        entity_1 = Entity("TEST")

        db.session.add(entity_1)
        db.session.commit()

        first_call = entity_1.test_cached_fn()
        second_call = entity_1.test_cached_fn()

        self.assertEqual(first_call, second_call)
        db.session.delete(entity_1)
        db.session.commit()

    def test_instance_cache_change(self):
        entity_1 = Entity("TEST")

        db.session.add(entity_1)
        db.session.commit()

        first_call = entity_1.test_cached_fn(1)
        second_call = entity_1.test_cached_fn(2)

        self.assertNotEqual(first_call, second_call)

        db.session.delete(entity_1)
        db.session.commit()

    def test_instance_cache_property_set(self):
        VALUE = 'test-test'
        entity_1 = Entity("TEST")

        db.session.add(entity_1)
        db.session.commit()

        first_call = entity_1.test_cached_prop
        entity_1.test_cached_prop = VALUE
        second_call = entity_1.test_cached_prop

        self.assertNotEqual(first_call, VALUE)
        self.assertEqual(second_call, VALUE)
        db.session.delete(entity_1)
        db.session.commit()

    def test_instance_cache_property_clean(self):
        VALUE = 'test-test'
        entity_1 = Entity("TEST")

        db.session.add(entity_1)
        db.session.commit()

        first_call = entity_1.test_cached_prop
        entity_1.test_cached_prop = VALUE
        second_call = entity_1.test_cached_prop
        entity_1.cache.clear()
        third_call = entity_1.test_cached_prop

        self.assertNotEqual(first_call, VALUE)
        self.assertEqual(second_call, VALUE)
        self.assertNotEqual(third_call, VALUE)

        db.session.delete(entity_1)
        db.session.commit()
