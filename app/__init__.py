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
from config import twitter_api

oauth = OAuth(app)
twitter = oauth.remote_app(
	'twitter',
	consumer_key = '0yh6Qo6xtrGh0lVMlOfrQ',
	consumer_secret = 'MXGHuH1BoIRRl6lwCIiiZa9McdR55rMvXYaCBuWZXxU',
	base_url = 'https://api.twitter.com/1.1/',
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	authorize_url = 'https://api.twitter.com/oauth/authenticate',
)

oauth.init_app(app)

from app import views

