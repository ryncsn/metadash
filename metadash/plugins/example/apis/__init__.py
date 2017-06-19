from flask import Blueprint
from flask_restful import Resource, Api
from ..models import ExampleEntity
from metadash.models import db, get_or_create


Blueprint = Blueprint('example', __name__)

Api = Api(Blueprint)


class ExampleAPI(Resource):
    def get(self):
        instance, _ = get_or_create(db.session, ExampleEntity, name="Plugin: Hello, World!")
        if _:
            db.session.commit()
        dict_ = instance.as_dict()
        dict_['cached_function'] = instance.cached_function()
        dict_['cached_property'] = instance.cached_property
        return dict_


Api.add_resource(ExampleAPI, '/example/', endpoint='example')
