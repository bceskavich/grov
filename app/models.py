from app import db, app

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True) # Twitter's 'screen_name'
	# Twitter's 'user_id'
	twitter_id = db.Column(db.Integer, index = True, unique = True)
	# Twitter's 'oauth_token'
	access_token = db.Column(db.String(64), unique = True)
	# Twitter's 'oauth_token_secret'
	access_secret = db.Column(db.String(64), unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)

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