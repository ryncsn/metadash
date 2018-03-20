Deploy and scale
====================================

In the previous session, we talked about how to set up a development environment, but it's not suitable for production environment.

When deploying for a production environment, please consider following suggestions and steps:

- PostgreSQL server, Redis server, Celery workers are required, please following related documents and setup thoes services.
- Custom configurations listed in config/__init__.py (by setting environmental variables), let Metadash be able to connect to PostgreSQL, Redis.
- DO REMEMBER to set your secret key in config/config.py.

- Set configurations by environmental variables.
- Start Celery workers as required.
- Use a wsgi host server like uWSGI.
- uWSGI server and Celery workers are scaleable, please adjust the number of uWSGI workers and Celery workers to meet your requirements.
