from flask import Blueprint, request
from flask_restful import Resource, Api, abort

from ..models import TestResult, TestCase, TestGroup
from metadash.models import db
from metadash.apis import default_entity_parser

TestGroupParser = default_entity_parser(TestGroup)
TestGroupParser.add_argument('descrition', type=str, required=True, location='json')
TestGroupParser.add_argument('ref_url', type=str, default='', location='json')

TestResultParser = default_entity_parser(TestResult)
TestResultParser.add_argument('outcome', type=str, required=True, location='json')
TestResultParser.add_argument('testcase', type=str, required=True, location='json')
TestResultParser.add_argument('testgroups', type=list, required=True, location='json', default=[])
TestResultParser.add_argument('ref_url', type=str, required=True, location='json')

Blueprint = Blueprint('results-db', __name__)

Api = Api(Blueprint)


class TestCaseList(Resource):
    def get(self):
        return [result.as_dict() for result in TestCase.query.all()]


class TestResultList(Resource):
    def post(self):
        args = TestResultParser.parse_args()
        result = TestResult()
        result.from_dict(args)
        result.tags.append("statistic")
        db.session.add(result)
        db.session.commit()
        return result.as_dict()

    def get(self):
        return TestResult.fetch(**request.args)  # TODO: Danger!!!


class TestResultDetail(Resource):
    def get(self, uuid_):
        result = TestResult.query.get(uuid_)
        if not result:
            abort(404, message="TestResult {} doesn't exist".format(uuid_))
        return result.as_dict()


class TestGroupList(Resource):
    def post(self):
        args = TestGroupParser.parse_args()
        group = TestGroup()
        group.from_dict(args)
        group.tags.append("statistic")
        db.session.add(group)
        db.session.commit()
        return group.as_dict()

    def get(self):
        return [group.as_dict() for group in TestGroup.query.all()]


class TestGroupDetail(Resource):
    def put(self, uuid_):
        group = TestGroup.query.get(uuid_)
        if not group:
            abort(404, message="TestGroup {} doesn't exist".format(uuid_))
        args = TestGroupParser.parse_args()
        group.from_dict(args)
        db.session.commit()
        return group.as_dict(detail=True)

    def get(self, uuid_):
        group = TestGroup.query.get(uuid_)
        if not group:
            abort(404, message="TestGroup {} doesn't exist".format(uuid_))
        return group.as_dict(detail=True)


Api.add_resource(TestCaseList, '/cases/', endpoint='cases')
Api.add_resource(TestResultList, '/results/', endpoint='results')
Api.add_resource(TestResultDetail, '/results/<uuid_>', endpoint='result_details')
Api.add_resource(TestGroupList, '/groups/', endpoint='groups')
Api.add_resource(TestGroupDetail, '/groups/<uuid_>', endpoint='group_details')
