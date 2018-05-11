"""
Basic test boilerplate
"""
from . import BasicTestCase
from metadash.models import db
from metadash.models.base import EntityModel, AttributeModel


class Entity(EntityModel):
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'metadash-test-entity'

    # Key in resultsdb
    value = db.Column(db.String(), primary_key=True, unique=True, index=True)

    def __init__(self, value):
        self.value = value

    def as_dict(self, **kwargs):
        ret = super(Entity, self).as_dict(**kwargs)
        return ret


class Attribute(AttributeModel):
    """
    Stands for a test case
    """
    __tablename__ = 'metadash-test-attribute'

    # Key in resultsdb
    key = db.Column(db.String(), primary_key=True, unique=True)
    value = db.Column(db.String())

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def as_dict(self, **kwargs):
        ret = super(Attribute, self).as_dict(**kwargs)
        return ret


class EntityTest(BasicTestCase):
    def test_entity_create(self):
        VALUE = 'entity1'
        entity = Entity(VALUE)
        db.session.add(entity)
        db.session.commit()

        entity = Entity.query.filter(Entity.value == VALUE).first()
        assert entity.as_dict()['value'] == VALUE

    def test_entity_default_attributes(self):
        VALUE = 'entity1'
        entity = Entity(VALUE)
        entity.properties = {
            "prop1": "prop_value1",
            "prop2": [
                "prop_value2_1",
                "prop_value2_2",
            ]
        }
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        assert entity.as_dict()['value'] == VALUE
        assert entity.as_dict()['properties']['prop1'] == 'prop_value1'
        assert entity.as_dict()['properties']['prop2'][0] == 'prop_value2_1'
        assert entity.as_dict()['properties']['prop2'][1] == 'prop_value2_2'
