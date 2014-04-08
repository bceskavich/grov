from flask import Response, jsonify
import twitter, json, os
from app import db, app
from config import CONSUMER_KEY, CONSUMER_SECRET
import networkx as nx
from networkx.readwrite import json_graph

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True) # Twitter's 'screen_name'
	# Twitter's 'user_id'
	twitter_id = db.Column(db.String(256), index = True, unique = True)
	# Twitter's 'oauth_token'
	access_token = db.Column(db.String(64), unique = True)
	# Twitter's 'oauth_token_secret'
	access_secret = db.Column(db.String(64), unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	connections = db.relationship('Connection', backref='user', lazy='dynamic')

	# Generates a Twitter API object for querying
	def oauth_login(self):
		# Four parameters needed for OAuth object
		CKEY = CONSUMER_KEY
		CSECRET = CONSUMER_SECRET
		OTOKEN = self.access_token
		OSECRET = self.access_secret

		# Generates twitter api object
		auth = twitter.oauth.OAuth(OTOKEN, OSECRET, CKEY, CSECRET)
		twitter_api = twitter.Twitter(auth=auth)

		return twitter_api

	# Checks if new connection is already in the DB
	def is_unique(self, connection, rel):
		# Finds saved connections, by current user + relationship type + id
		saved = Connection.query.filter_by(user_id=self.id, rel=rel, twitter_id=connection)
		# Returns False if connection already exists in DB
		if len(saved.all()) > 0:
			return False
		else:
			return True

	def get_connections(self):
		# Initiates Twitter API connections
		twitter_api = self.oauth_login()

		# Gets "friends" and followers lists from Twitter
		# Max limited to 1500 for the sake of this project and the node graph size
		friends = twitter_api.friends.ids(count=1500)
		followers = twitter_api.followers.ids(count=1500)

		# Counts to determine how many are saved
		frnd_count = 0
		foll_count = 0

		# Saves connection to DB only if new
		# Adds one to the count of saved friends
		for friend in friends['ids']:
			if self.is_unique(str(friend), rel=1):
				connection = Connection(twitter_id=str(friend), rel=1, user_id=self.id)
				db.session.add(connection)
				db.session.commit()
				frnd_count += 1

		# Saves connection to DB only if new
		# Adds one to the count of saved followers
		for follower in followers['ids']:
			if self.is_unique(str(follower), rel=0):
				connection = Connection(twitter_id=str(follower), rel=0, user_id=self.id)
				db.session.add(connection)
				db.session.commit()
				foll_count += 1

		# Returns counts of saved friends and followers
		return frnd_count, foll_count

	def create_graph(self):
		# Initiate Graph
		g = nx.DiGraph()

		twitter_ids = [u.twitter_id for u in User.query.all()]

		for user in User.query.all():
			amnt = 1
			if len(Connection.query.filter_by(twitter_id=user.twitter_id).all()) > 0:
				amnt += len(Connection.query.filter_by(twitter_id=user.twitter_id).all())
			g.add_node(user.twitter_id, {'label':'@' + user.username, 'amnt':amnt, 'class':'user' })

		for conn in Connection.query.all():
			if conn.twitter_id in twitter_ids:
				pass
			elif conn.rel == 0:
				amnt = len(Connection.query.filter_by(twitter_id=conn.twitter_id).all())
				g.add_node(conn.twitter_id, {
					'label':'Anonymous Follower',
					'user_id':conn.user_id,
					'amnt':amnt,
					'class':'anonymous' })
			elif conn.rel == 1:
				amnt = len(Connection.query.filter_by(twitter_id=conn.twitter_id).all())
				g.add_node(conn.twitter_id, {
					'label':'Anonymous Friend',
					'user_id':conn.user_id,
					'amnt':amnt,
					'class':'anonymous' })


		friends = Connection.query.filter_by(rel=1)
		followers = Connection.query.filter_by(rel=0)

		for i in friends:
			user = User.query.get(i.user_id)
			g.add_edge(i.twitter_id, user.twitter_id)

		for i in followers:
			user = User.query.get(i.user_id)
			g.add_edge(user.twitter_id, i.twitter_id)

		data = json_graph.dumps(g, encoding='utf-8')
		f = file('app/static/json/graphdata.json', 'w')
		f.write(data)
		f.close()

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)

class Connection(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	twitter_id = db.Column(db.String(256), index = True)
	name = db.Column(db.String(64), index = True)
	rel = db.Column(db.SmallInteger) # 0 = follower, 1 = friend, 2 = recursive
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
