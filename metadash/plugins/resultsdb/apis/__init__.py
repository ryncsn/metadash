from flask import Blueprint, request
from flask_restful import Resource, Api, abort

from ..models import ResultsDBTestResult, ResultsDBTestCase, ResultsDBTestGroup
from metadash.models import db
from metadash.apis import EntityParser

ResultsDBTestGroupParser = EntityParser(ResultsDBTestGroup)
ResultsDBTestGroupParser.add_argument('descrition', type=str, required=True, location='json')
ResultsDBTestGroupParser.add_argument('ref_url', type=str, default='', location='json')

ResultsDBTestResultParser = EntityParser(ResultsDBTestResult)
ResultsDBTestResultParser.add_argument('outcome', type=str, required=True, location='json')
ResultsDBTestResultParser.add_argument('testcase', type=str, required=True, location='json')
ResultsDBTestResultParser.add_argument('testgroups', type=list, required=True, location='json', default=[])
ResultsDBTestResultParser.add_argument('ref_url', type=str, required=True, location='json')

Blueprint = Blueprint('results-db', __name__)

Api = Api(Blueprint)


class ResultsDBTestCaseList(Resource):
    def get(self):
        return [result.as_dict() for result in ResultsDBTestCase.query.all()]


class ResultsDBTestResultList(Resource):
    def post(self):
        args = ResultsDBTestResultParser.parse_args()
        result = ResultsDBTestResult()
        result.from_dict(args)
        result.tags.append("statistic")
        db.session.add(result)
        db.session.commit()
        return result.as_dict()

    def get(self):
        return ResultsDBTestResult.fetch(**request.args)  # TODO: Danger!!!


class ResultsDBTestResultDetail(Resource):
    def get(self, uuid_):
        result = ResultsDBTestResult.query.get(uuid_)
        if not result:
            abort(404, message="ResultsDBTestResult {} doesn't exist".format(uuid_))
        return result.as_dict()


class ResultsDBTestGroupList(Resource):
    def post(self):
        args = ResultsDBTestGroupParser.parse_args()
        group = ResultsDBTestGroup()
        group.from_dict(args)
        group.tags.append("statistic")
        db.session.add(group)
        db.session.commit()
        return group.as_dict()

    def get(self):
        return [group.as_dict() for group in ResultsDBTestGroup.query.all()]


class ResultsDBTestGroupDetail(Resource):
    def put(self, uuid_):
        group = ResultsDBTestGroup.query.get(uuid_)
        if not group:
            abort(404, message="ResultsDBTestGroup {} doesn't exist".format(uuid_))
        args = ResultsDBTestGroupParser.parse_args()
        group.from_dict(args)
        db.session.commit()
        return group.as_dict(detail=True)

    def get(self, uuid_):
        group = ResultsDBTestGroup.query.get(uuid_)
        if not group:
            abort(404, message="ResultsDBTestGroup {} doesn't exist".format(uuid_))
        return group.as_dict(detail=True)


Api.add_resource(ResultsDBTestCaseList, '/cases/', endpoint='cases')
Api.add_resource(ResultsDBTestResultList, '/results/', endpoint='results')
Api.add_resource(ResultsDBTestResultDetail, '/results/<uuid_>', endpoint='result_details')
Api.add_resource(ResultsDBTestGroupList, '/groups/', endpoint='groups')
Api.add_resource(ResultsDBTestGroupDetail, '/groups/<uuid_>', endpoint='group_details')
