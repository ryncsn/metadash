#!/usr/bin/env python
import coloredlogs

coloredlogs.install(level='INFO')

# Load Flask
from metadash import app, db  # noqa

# Load Manager and Migration
from flask_migrate import Migrate, MigrateCommand  # noqa
from flask_script import Manager  # noqa

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
@manager.option('-t', '--testcase', dest='testcase')
def test_api(testcase=None):
    import unittest
    import os
    from metadash import plugins

    suite = unittest.TestSuite()
    loader = unittest.loader.defaultTestLoader

    if testcase:
        try:
            suite.addTests(loader.loadTestsFromName(testcase))
        except ModuleNotFoundError:
            return "Python test case not found"
        else:
            pass
    else:
        suite.addTests(loader.loadTestsFromName("metadash.test.api"))

        for file in os.listdir('metadash/test/api'):
            if not file.startswith('_') and not file.startswith('.') and file.endswith('.py'):
                suite.addTests(loader.loadTestsFromName("metadash.test.api.{}".format(file[:-3])))

        for plugin_name, plugin in plugins.get_all().items():
            try:
                __import__(plugin['import'] + '.tests')
            except ModuleNotFoundError:
                pass
            else:
                suite.addTests(loader.loadTestsFromName(plugin['import'] + '.tests'))

    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return len(result.errors + result.failures)


@manager.command
@manager.option('-n', '--name', dest='name')
@manager.option('-p', '--password', dest='password')
def create_user(username=None, password=None):
    """
    reate or overlay a user with local authentication
    """
    if username and password:
        from metadash.auth import user_signup
        user_signup(username, password, 'local')
    else:
        raise "Username and password required"


@manager.command
def initdb():
    init_db()


def init_db():
    with app.app_context():
        db.create_all()


# Start the manager
if __name__ == '__main__':
    manager.run()
