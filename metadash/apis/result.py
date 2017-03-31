import datetime
import uuid

from flask import Blueprint
from flask_restful import reqparse, Resource, Api, abort

from metadash.models.result import TestResult, TestRun
from metadash import db

TestResultParser = reqparse.RequestParser(bundle_errors=True)
TestResultParser.add_argument('result', type=lambda _s: TestResult.ALL_RESULTS.index(_s) + 1 and _s, required=True)
TestResultParser.add_argument('date', type=datetime.datetime, required=False)
TestResultParser.add_argument('test_run', type=uuid.UUID, required=True)

TestRunParser = reqparse.RequestParser(bundle_errors=True)
TestRunParser.add_argument('name', type=str, required=True)

Blueprint = Blueprint('result', __name__)

Api = Api(Blueprint)


class TestResultList(Resource):
    def post(self):
        result = TestResult()
        args = TestResultParser.parse_args()
        result.test_run = args['test_run']
        result.result = args['result']
        result.date = args['date']
        db.session.add(result)
        db.session.commit()
        return result.as_dict(detail=True)

    def get(self):
        return [run.as_dict(detail=True) for run in TestResult.query.all()]


class TestResultDetail(Resource):
    def delete(self, uuid_):
        result = TestResult.query.get(uuid_)
        if not result:
            abort(404, message="TestResult {} doesn't exist".format(uuid_))
        db.session.delete(result)
        db.session.commit()
        return '', 204

    def put(self, uuid_):
        result = TestResult.query.get(uuid_)
        args = TestResultParser.parse_args()
        result.test_run = args['test_run']
        result.result = args['result']
        result.date = args['date']
        if not result:
            abort(404, message="TestResult {} doesn't exist".format(uuid_))
        return result.as_dict(detail=True)

    def get(self, uuid_):
        result = TestResult.query.get(uuid_)
        if not result:
            abort(404, message="TestResult {} doesn't exist".format(uuid_))
        return result.as_dict(detail=True)


class TestRunList(Resource):
    def post(self):
        run = TestRun()
        args = TestRunParser.parse_args()
        run.name = args['name']
        db.session.add(run)
        db.session.commit()
        return run.as_dict(detail=True)

    def get(self):
        return [run.as_dict(detail=True) for run in TestRun.query.all()]


class TestRunDetail(Resource):
    def delete(self, uuid_):
        run = TestRun.query.get(uuid_)
        if not run:
            abort(404, message="TestRun {} doesn't exist".format(uuid_))
        db.session.delete(run)
        db.session.commit()
        return '', 204

    def put(self, uuid_):
        run = TestRun.query.get(uuid_)
        args = TestRunParser.parse_args()
        run.name = args['name']
        if not run:
            abort(404, message="TestRun {} doesn't exist".format(uuid_))
        return run.as_dict(detail=True)

    def get(self, uuid_):
        run = TestRun.query.get(uuid_)
        if not run:
            abort(404, message="TestRun {} doesn't exist".format(uuid_))
        return run.as_dict(detail=True)


Api.add_resource(TestResultList, '/result/', endpoint='result')
Api.add_resource(TestResultDetail, '/result/<uuid>', endpoint='result_detail')
Api.add_resource(TestRunList, '/run/', endpoint='run')
Api.add_resource(TestRunDetail, '/run/<uuid>', endpoint='run_detail')
