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
    value = db.Column(db.String())

    def __init__(self, value):
        self.value = value

    def as_dict(self, **kwargs):
        ret = super(Entity, self).as_dict(**kwargs)
        return ret


class EntityTest(BasicTestCase):
    def test_entity_with_properties(self):
        VALUE = 'entity1'
        PROPERTIES = {
            "prop1": "prop_value1",
            "prop2": [
                "prop_value2_1",
                "prop_value2_2",
                "prop_value2_3",
            ],
            "prop3": None,
        }

        entity = Entity(VALUE)
        entity.properties = PROPERTIES
        entity.properties['prop1'] = 'prop_value1'
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)
        db.session.delete(entity)
        db.session.commit()

    def test_entity_modify_properties(self):
        VALUE = 'entity1'
        PROPERTIES = {
            "prop1": "prop_value1",
            "prop2": [
                "prop_value2_1",
                "prop_value2_2",
                "prop_value2_3",
            ],
            "prop3": None,
        }

        entity = Entity(VALUE)
        entity.properties = PROPERTIES
        entity.properties['prop1'] = 'prop_value1'
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)

        PROPERTIES["prop2"].append("prop_value2_4")
        entity.properties["prop2"].append("prop_value2_4")

        PROPERTIES["prop2"].remove("prop_value2_1")
        entity.properties["prop2"].remove("prop_value2_1")

        PROPERTIES["prop3"] = "prop_value3"
        entity.properties["prop3"] = "prop_value3"

        PROPERTIES["prop4"] = "prop_value4"
        entity.properties["prop4"] = "prop_value4"

        db.session.commit()
        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)
