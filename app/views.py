from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_oauthlib.client import OAuth
from app import app, db, login_manager, twitter, oauth
from models import User, ROLE_USER, ROLE_ADMIN
import json
import requests

@app.before_request
def before_request():
	g.user = None
	if 'twitter' in session:
		g.user = current_user

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
	title = "Grov - A Work In Progress"
	head = "THIS IS GROV"
	if g.user is not None and g.user.is_authenticated():
		frnd_count, foll_count = g.user.get_connections()
		print "Saved " + str(frnd_count) + " friends."
		print "Saved " + str(foll_count) + " followers."
	return render_template("index.html",
		title = title,
		head = head)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	return twitter.authorize(callback=url_for('auth', 
		next=request.args.get('next') or request.referrer or None))

@app.route('/auth', methods = ['GET', 'POST'])
@twitter.authorized_handler
def auth(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None:
		flash(u"Ah shit, something went wrong.")
		return redirect(next_url)
	print json.dumps(resp, indent=1)
	user = User.query.filter_by(username = resp['screen_name']).first()
	if user is None:
		user = User(username = resp['screen_name'], 
			twitter_id = resp['user_id'], 
			access_token = resp['oauth_token'], 
			access_secret = resp['oauth_token_secret'])
		db.session.add(user)
		db.session.commit()
	login_user(user)
	session['twitter'] = resp
	return redirect(next_url)

@app.route('/logout')
def logout():
	logout_user()
	session.pop('twitter', None)
	return redirect(url_for('index'))
