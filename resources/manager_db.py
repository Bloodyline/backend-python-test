from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from alayatodo import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from alayatodo.orm import Users, Todos

# Run the db manager
def manager_run():
    manager.run()