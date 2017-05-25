import datetime
import uuid

from flask import Blueprint
from flask_restful import reqparse, Resource, Api, abort

from metadash.models.results import TestResult, TestCase, TestGroup
from metadash import db

TestGroupParser = reqparse.RequestParser(bundle_errors=True)
TestGroupParser.add_argument('descrition', type=str, required=True)
TestGroupParser.add_argument('ref_url', type=str, default='')

TestResultParser = reqparse.RequestParser(bundle_errors=True)
TestResultParser.add_argument('outcome', type=str, required=True)
TestResultParser.add_argument('testcase', type=str, required=True)
TestResultParser.add_argument('testgroups', type=str, required=True, action='append')
TestResultParser.add_argument('ref_url', type=str, required=True)

TestGroupParser = reqparse.RequestParser(bundle_errors=True)
TestGroupParser.add_argument('description', type=str, required=True)

Blueprint = Blueprint('result', __name__)

Api = Api(Blueprint)


class TestResultList(Resource):
    def post(self):
        result = TestResult()
        args = TestResultParser.parse_args()
        result.testcase = args['testcase']
        result.testgroups = args['testgroups']
        result.ref_url = args['ref_url']
        result.outcome = args['outcome']
        db.session.add(result)
        db.session.commit()
        return result.as_dict(detail=True)

    def get(self):
        return [result.as_dict(detail=True) for result in TestResult.query.all()]


class TestResultDetail(Resource):
    def get(self, uuid_):
        result = TestResult.query.get(uuid_)
        if not result:
            abort(404, message="TestResult {} doesn't exist".format(uuid_))
        return result.as_dict(detail=True)


class TestGroupList(Resource):
    def post(self):
        group = TestGroup()
        args = TestGroupParser.parse_args()
        group.description = args['description']
        db.session.add(group)
        db.session.commit()
        return group.as_dict(detail=True)

    def get(self):
        return [group.as_dict(detail=True) for group in TestGroup.query.all()]


class TestGroupDetail(Resource):
    def put(self, uuid_):
        group = TestGroup.query.get(uuid_)
        if not group:
            abort(404, message="TestGroup {} doesn't exist".format(uuid_))
        args = TestGroupParser.parse_args()
        group.description = args['description']
        db.session.commit()
        return group.as_dict(detail=True)

    def get(self, uuid_):
        group = TestGroup.query.get(uuid_)
        if not group:
            abort(404, message="TestGroup {} doesn't exist".format(uuid_))
        return group.as_dict(detail=True)


Api.add_resource(TestResultList, '/result/', endpoint='result')
Api.add_resource(TestResultDetail, '/result/<uuid_>', endpoint='result_detail')
Api.add_resource(TestGroupList, '/group/', endpoint='group')
Api.add_resource(TestGroupDetail, '/group/<uuid_>', endpoint='group_detail')
