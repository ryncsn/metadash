import uuid
from flask import Blueprint
from flask_restful import reqparse, Resource, Api

from metadash.models.metadata import Property, Detail, Tag
from metadash import db

Blueprint = Blueprint('metadata', __name__)

Api = Api(Blueprint)

PropertyParser = reqparse.RequestParser(bundle_errors=True)
PropertyParser.add_argument('key', type=str, required=True)
PropertyParser.add_argument('value', type=str, required=True)
PropertyParser.add_argument('parent', type=uuid.UUID, required=True)


TagParser = reqparse.RequestParser(bundle_errors=True)
TagParser.add_argument('name', type=str, required=True)
TagParser.add_argument('parents', action='append', default=[], required=False)


class PropertyList(Resource):
    def post(self):
        args = PropertyParser.parse_args()
        property_ = Property()
        property_.key = args['key']
        property_.value = args['value']
        property_.parent = args['parent']
        db.session.add(property_)
        db.session.commit()

    def get(self):
        return [prop.as_dict(detail=True) for prop  in Property.query.all()]


class TagList(Resource):
    def post(self):
        args = TagParser.parse_args()
        tag = Tag()
        tag.name = args['name']
        tag.parents = args['parents']
        db.session.add(tag)
        db.session.commit()

    def get(self):
        return [tag.as_dict(detail=True) for tag in Tag.query.all()]


Api.add_resource(PropertyList, '/property/', endpoint='properties')
Api.add_resource(TagList, '/tag/', endpoint='tags')
