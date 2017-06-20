import uuid

from flask_restful import reqparse


def default_entity_parser(entity=None):
    EntityParser = reqparse.RequestParser(bundle_errors=True)
    EntityParser.add_argument('uuid', type=uuid, location='json')
    EntityParser.add_argument('ref_url', type=str, location='json')
