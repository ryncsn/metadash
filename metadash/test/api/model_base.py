"""
Basic test boilerplate
"""
from . import BasicTestCase
from metadash.models import db
from metadash.models.base import EntityModel, BareEntityModel


class Entity(EntityModel):
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'metadash-test-entity'

    value = db.Column(db.String())

    def __init__(self, value):
        self.value = value


class BareEntity(BareEntityModel):
    """
    Stands for a test case
    """
    __namespace__ = 'metadash-test-bareentity'


class EntityTest(BasicTestCase):  # pragma: no cover
    def test_bareentity_with_properties(self):
        PROPERTIES = {
            "prop1": "prop_value1",
            "prop2": [
                "prop_value2_1",
                "prop_value2_2",
                "prop_value2_3",
            ],
            "prop3": None,
        }

        entity = BareEntity()
        entity.properties = PROPERTIES
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = BareEntity.query.first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)
        db.session.delete(entity)
        db.session.commit()

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
        }

        entity = Entity(VALUE)
        entity.properties = PROPERTIES
        entity.properties['prop2'] = 'prop_value2'
        PROPERTIES['prop2'] = 'prop_value2'
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)

        del PROPERTIES["prop1"]
        del entity.properties["prop1"]

        PROPERTIES["prop3"] = "prop_value3"
        entity.properties["prop3"] = "prop_value3"

        db.session.commit()
        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)

    def test_entity_modify_proxied_properties(self):
        VALUE = 'entity1'
        PROPERTIES = {
            "prop1": [
                "prop_value1_1",
                "prop_value1_2",
                "prop_value1_3",
                "prop_value1_4",
                "prop_value1_5",
            ],
            "prop2": "prop2_value"
        }

        entity = Entity(VALUE)
        entity.properties = PROPERTIES
        db.session.add(entity)
        db.session.commit()

        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertDictEqual(dict(entity.properties), PROPERTIES)

        PROPERTIES["prop1"].append("prop_value1_6")
        entity.properties["prop1"].append("prop_value1_6")

        PROPERTIES["prop1"].remove("prop_value1_1")
        entity.properties["prop1"].remove("prop_value1_1")

        del PROPERTIES["prop1"][0]
        del entity.properties_ref["prop1"][0]

        PROPERTIES["prop1"][0] = "set_prop"
        entity.properties["prop1"][0] = "set_prop"

        PROPERTIES["prop1"].pop()
        entity.properties_ref["prop1"].pop()

        PROPERTIES.remove("prop2")
        entity.properties.remove("prop2")

        db.session.commit()
        entity = None
        entity = Entity.query.filter(Entity.value == VALUE).first()
        self.assertEqual(set(entity.properties["prop1"]), set(PROPERTIES["prop1"]))

        db.session.delete(entity)
        db.session.commit()

    def test_entity_modify_proxied_properties(self):
        VALUE = 'entity1'

        entity = Entity(VALUE)

        exception = None

        try:
            entity.properties['NON_EXIST']
        except KeyError as error:
            exception = error

        self.assertIn("NON_EXIST", str(exception))
