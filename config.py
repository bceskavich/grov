import os

CSRF_ENABLED = True
SECRET_KEY = 't0h1e0s1k0i1e0s1a0w1a0i1t0'

basedir = os.path.abspath(os.path.dirname(__file__))

# Path of the database file
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Path where we store the migration data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CONSUMER_KEY = '0yh6Qo6xtrGh0lVMlOfrQ'
CONSUMER_SECRET = 'MXGHuH1BoIRRl6lwCIiiZa9McdR55rMvXYaCBuWZXxU'
