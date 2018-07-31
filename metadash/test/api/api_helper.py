"""
Basic test boilerplate
"""
import json
import datetime

from . import BasicTestCase

from flask import Blueprint
from flask_restful import Resource, Api

from metadash import app
from metadash.models import db
from metadash.models.base import EntityModel
from metadash.apis import EntityParser, pager, envolop


class TestResource(EntityModel):  # pragma: no cover
    """
    Stands for a test case
    """
    __tablename__ = __alias__ = __namespace__ = 'metadash-test-resource'

    attr_1 = db.Column(db.String(), nullable=False)
    attr_2 = db.Column(db.String())
    attr_3 = db.Column(db.DateTime())

    def as_dict(self, **kwargs):
        ret = super(TestResource, self).as_dict(**kwargs)
        return ret


TestResourceParser = EntityParser(TestResource)


class TestResourceAPI(Resource):
    def get(self):
        args = TestResourceParser.parse_extra()
        return envolop(
            [result.as_dict() for result in pager(TestResource.query.filter_by(**args)).all()],
        )

    def post(self):
        args = TestResourceParser.parse_args()
        testcase = TestResource.from_dict(args)
        db.session.add(testcase)
        db.session.commit()
        return testcase.as_dict()


Blueprint = Blueprint('test-resource', __name__)
Api(Blueprint).add_resource(TestResourceAPI, '/', endpoint='_test_resource')
app.register_blueprint(Blueprint, url_prefix='/_test_resource')


class APIHelperTest(BasicTestCase):  # pragma: no cover
    def _query(self, data):
        rv = self.app.get(
            '/_test_resource/', data=json.dumps(data),
            content_type='application/json'
        )
        return rv

    def test_create(self):
        DATA = {
            "attr_1": "attr_1_value",
            "attr_2": "attr_2_value",
            "attr_3": datetime.datetime.now().isoformat(),
            "properties": {
                "meta1": "meta_value1"
            },
            "tags": ["tag_1", "tag_2"]
        }
        rv = self.app.post(
            '/_test_resource/', data=json.dumps(DATA),
            content_type='application/json'
        )
        data = json.loads(rv.data.decode())
        data['attr_3'] = data['attr_3'].replace(' ', 'T')
        DATA['tags'] = set(DATA['tags'])
        data['tags'] = set(data['tags'])

        self.assertDictContainsSubset(DATA, data)

    def test_get_paged(self):
        for number in range(100):
            DATA = {
                "attr_1": "attr_1_value_{}".format(number),
                "attr_2": "attr_2_value_{}".format(number % 10),
                "properties": {
                    "meta1": "meta_value_{}".format(number),
                    "meta2": "meta_value_{}".format(number % 10)
                }
            }
            self.app.post(
                '/_test_resource/', data=json.dumps(DATA),
                content_type='application/json'
            )

        rv = self.app.get('/_test_resource/?limit=35')
        data = json.loads(rv.data.decode())
        self.assertEqual(len(data['data']), 35)

        rv = self.app.get(data['next'])
        self.assertEqual(len(json.loads(rv.data.decode())['data']), 35)
