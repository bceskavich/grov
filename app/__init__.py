from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import os
from flask.ext.login import LoginManager
from config import basedir

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask_oauthlib.client import OAuth
from config import CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(app)
twitter = oauth.remote_app(
	'twitter',
	consumer_key = CONSUMER_KEY,
	consumer_secret = CONSUMER_SECRET,
	base_url = 'https://api.twitter.com/1.1/',
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	authorize_url = 'https://api.twitter.com/oauth/authorize'
)

oauth.init_app(app)

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('GROV')

from app import views

