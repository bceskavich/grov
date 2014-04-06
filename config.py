import os

CSRF_ENABLED = True

basedir = os.path.abspath(os.path.dirname(__file__))

# Heroku vs. Local Configurations
if os.environ.get('HEROKU') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # CSRF Key
    SECRET_KEY = os.environ['CSRF_SECRET_KEY']

    # Twitter API Credentials
    CONSUMER_KEY = os.environ['TWITTER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_SECRET']
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # CSRF Key
    SECRET_KEY = 't0h1e0s1k0i1e0s1a0w1a0i1t0'

    # Twitter API Credentials
    CONSUMER_KEY = '0yh6Qo6xtrGh0lVMlOfrQ'
    CONSUMER_SECRET = 'MXGHuH1BoIRRl6lwCIiiZa9McdR55rMvXYaCBuWZXxU'

# Path where we store the migration data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

