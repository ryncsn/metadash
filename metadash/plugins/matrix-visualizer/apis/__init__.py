from flask import Blueprint, jsonify
from flask_restful import Resource, Api

from metadash.models.base.registry import EntityRegistry
from metadash.apis import EntityParser, pager, envolop
from metadash.models.metadata import Property

app = Blueprint = Blueprint('matrix-visualizer', __name__)

Api = Api(Blueprint)


class EntityModels(Resource):
    """
    Helper to get all entities sotred in Metadash and their API path
    """
    def get(self):
        ret = {}
        for name, entity in EntityRegistry.items():
            properties = entity.cache.get_or_create('all_property_keys', lambda: Property.all_keys(entity))
            ret[name] = {
                'properties': properties
            }
        return jsonify(ret)


class EntityList(Resource):
    """
    Helper to get all entities sotred in Metadash and their API path
    """
    def get(self, entity):
        if entity not in EntityRegistry.keys():
            return jsonify({
                "message": "Non-exist entity name {}".format(entity)
            })
        else:
            entity = EntityRegistry[entity]
            entity_parser = EntityParser(entity)
            args = entity_parser.parse_args()
            q = entity.query.filter_by(**args)
            q = pager(q)
            return envolop([
                e.as_dict(exclude=['details', 'tags']) for e in q.all()
            ])

    # TODO
    # def post(self, entity):
    #     pass

    # TODO
    # def put(self, entity):
    #     pass


Api.add_resource(EntityModels, '/matrix-visualizer/', endpoint='entity_models')
Api.add_resource(EntityList, '/matrix-visualizer/<entity>/', endpoint='entity_list')
