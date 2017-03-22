from flask import Blueprint
from flask_restful import reqparse, Resource, Api, abort

from metadash.models.result import AutoTestResult
from metadash import db

ResultParser = reqparse.RequestParser(bundle_errors=True)
ResultParser.add_argument('outcome', type=str, required=True)

Blueprint = Blueprint('result', __name__)

Api = Api(Blueprint)


class ResultList(Resource):
    def post(self):
        args = ResultParser.parse_args()
        result = AutoTestResult()
        result.outcome = args['outcome']
        db.session.add(result)
        db.session.commit()

    def get(self):
        return [run.as_dict(detail=True) for run in AutoTestResult.query.all()]


class ResultDetail(Resource):
    def delete(self, uuid):
        result = AutoTestResult.query.get(uuid)
        if not result:
            abort(404, message="AutoTestResult {} doesn't exist".format(uuid))
        db.session.delete(result)
        db.session.commit()
        return '', 204

    def get(self, uuid):
        result = AutoTestResult.query.get(uuid)
        if not result:
            abort(404, message="AutoTestResult {} doesn't exist".format(uuid))
        return result.as_dict(detail=True)


Api.add_resource(ResultList, '/', endpoint='result')
Api.add_resource(ResultDetail, '/<uuid>', endpoint='result_detail')
