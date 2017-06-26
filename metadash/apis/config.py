import uuid
from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from metadash.config import Config
from metadash import db
from metadash.auth import requires_roles

app = Blueprint = Blueprint('configs', __name__)

Api = Api(Blueprint)

ConfigParser = reqparse.RequestParser(bundle_errors=True)
ConfigParser.add_argument('value', type=str, required=False)


def _format(config):
    return {
        "key": config.key,
        "value": config.value,
        "plugin": config.plugin,
        "description": config.description,
        "nullable": config.nullable,
    }


class ConfigList(Resource):
    def get(self):
        return {
            "data": [
                _format(config)
                for config in Config.get_all()
            ]
        }


class ConfigDetail(Resource):
    @requires_roles('admin')
    def put(self, key):
        args = ConfigParser.parse_args()
        Config.set(key, args['value'])
        return _format(Config.get_config(key))

    def get(self, key):
        config = Config.get_config(key)
        return _format(config)


Api.add_resource(ConfigList, '/configs/', endpoint='config_list')
Api.add_resource(ConfigDetail, '/configs/<key>', endpoint='config_detail')
