from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    token = db.Column(db.Integer, index = True, unique = True) # OAuth access token
    username = db.Column(db.String(64), index = True, unique = True) # Corresponds to Twitter's 'screen_name'
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.username)