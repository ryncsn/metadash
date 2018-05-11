"""
Basic test boilerplate
"""
from . import BasicTestCase
from metadash.models import db
from metadash.models.base import EntityModel


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


class EntityTest(BasicTestCase):
    def test_entity_modify_properties(self):
        VALUE = 'entity1'
        PROPERTIES = {
            "prop1": "prop_value1",
            "prop2": [
                "prop_value2_1",
                "prop_value2_2",
            ]
        }

        entity = Entity(VALUE)
        entity.properties = PROPERTIES
        db.session.add(entity)
        db.session.commit()

        print(entity.properties)
