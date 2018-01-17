import time

from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from ..models import ExampleEntity
from metadash.models import db, get_or_create
from metadash.apis import EntityParser

from metadash.async import task
from metadash.async.task import update_task_info


app = Blueprint = Blueprint('example', __name__)

Api = Api(Blueprint)

ExampleParser = EntityParser(ExampleEntity)


def ensure_default_column():
    """
    Ensure there is at least one column for debug
    """
    instance, _ = get_or_create(db.session, ExampleEntity, name="Plugin: Hello, World!")
    if _:
        db.session.commit()


class ExampleAPI(Resource):
    def get(self):
        ensure_default_column()
        ret = []
        for row in ExampleEntity.query.all():
            dict_ = row.as_dict()
            dict_['cached_function'] = row.cached_function()
            dict_['cached_property'] = row.cached_property
            ret.append(dict_)
        return jsonify(ret)

    def post(self):
        args = ExampleParser.parse_args()
        example_entity = ExampleEntity()
        example_entity.from_dict(args)
        db.session.add(example_entity)
        db.session.commit()
        return jsonify(example_entity.as_dict())

    def put(self):
        instance, _ = get_or_create(db.session, ExampleEntity, name="Plugin: Hello, World!")
        if _:
            db.session.commit()
        dict_ = instance.as_dict()
        dict_['cached_function'] = instance.cached_function()
        dict_['cached_property'] = instance.cached_property
        return dict_


Api.add_resource(ExampleAPI, '/example/', endpoint='example')


@task()
def long_running(sleep_time):
    for i in range(sleep_time):
        update_task_info("RUNNING", "Sleeping (%s/%s)" % (i, sleep_time))
        time.sleep(1)
    return {
        "message": "Done!"
    }


@app.route('/example-task')
def start_task():
    long_running.delay(15)
    return jsonify({
        "message": "Task scheduled."
    })
