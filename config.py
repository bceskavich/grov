import os

CSRF_ENABLED = True
SECRET_KEY = 'enter-yours-here'

basedir = os.path.abspath(os.path.dirname(__file__))

# Path of the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# Path where we store the migration data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')