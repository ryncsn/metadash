#!/usr/bin/env python
# Load Flask
from metadash import app, db, socketio

# Load Manager and Migration
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    init_db()


def init_db():
    with app.app_context():
        db.create_all()


@manager.command
def runsocketio():
    socketio.run(app)


# Start the manager
if __name__ == '__main__':
    manager.run()
