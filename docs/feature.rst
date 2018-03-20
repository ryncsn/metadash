Feature & Performance
====================================

Metadash provides:

- A frontend framework based on Vue and Patternfly
- A backend framework based on Flask and SQLAlchemy
- Flexable ORM layer and Cache support
- Helpers for building RESTful API
- Async worker and perodic task support, and long running task support
- User authentication and permission control


ORM
---

Metadash used SQLAlchemy as the ORM layer, and introduced some helpers for easier implementing EAV support.
There are two pre-defined abstract models you can inherit from, metadash.models.entity and metadash.models.attribute.

All models inherit from metadash.models.attribute will have a relationship with models inherited from metadash.models.entity, unless explicitly restricted. The relaship could be accessed as attribute of the entity. The name of the attribute is pularized form of the attribute name in lower case.

Metadash predefined three models inherit from metadash.models.attribute, metadash.models.Property, metadash.models.Detail, metadash.models.Tag, so any model inherit from metadash.models.entity woould have three extra attributes ".details", ".properties", ".tag".

".properties" and ".details" are aggregated with a new introduces collection type, metadash.models.collections.attribute_mapped_list_collection, so you can access the attribute as a dictionary. And any dictionary operation works for the attribute. Values of the dictionary could be string or list of string.


API
-----

Metadash also provides helpers for defining RESTful API access for entities.


Cache
-----

Metadash provides helpers for caching.
For example, to have a better performance, entity's attribute which takes some time to load could be cached.
Each entity object have a .cache attribute, and it's simple to use. Use .cache.clear() to clean cache related to a entity, .cache.set(key, value), .cache.get_or_create(key, fn), .cache.get(key) to set or get cache of an entity.


Tasks
-----

For time-consuming tasks, like generate a bulk of cache, or wait for a message on the bus, you should define a task to do the job, and when cache regenerate or invalidation is required, just call the task with task.delay(\*args), then Celery workers will handle the task, and do the job in the background while not block the main server.


Long running tasks
------------------

You can also define forever running task, use @daemon decorator, and implement the task as usual. But @task.on_exit is required, else the task will always be force terminated on redeploy or shutdown. @task.on_exit will run in the same process as task function, so global variables are shared, you can use a global variable as a stop flag.


Permission Control
------------------

Metadash provides API level permission control. There are three roles in Metadash, admin, user, anonymous.
Refer to auth/__init__.py for more usage.


Frontend
--------

Metadash is a SPA (Single Page Application), and the frontend page use Vue as main framework.
Refer to "Setup Development Environment & Contribute" for more info.


You can use the example plugin as a reference of how to use some of the above features.
