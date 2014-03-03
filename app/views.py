from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, twitter
from models import User, ROLE_USER, ROLE_ADMIN
import json
import requests

@app.before_request
def before_request():
	g.user = None
	if 'twitter' in session:
		g.user = session['twitter']

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
	title = "Flask Foundation"
	head = "Welcome to Billy's Flask Foundation!"
	return render_template("index.html",
		title = title,
		head = head,
		user = g.user)

@app.route('/login')
def login():
	callback_url = url_for('oauthorized', next=request.args.get('next'))
	return twitter.authorize(callback=callback_url or request.referrer or None)

@app.route('/oauthorized')
@twitter.authorized_handler
def oauthorized(resp):
	if resp is None:
		flash("You've been denied access.")
	else:
		session['twitter'] = resp
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.pop('twitter', None)
	return redirect(url_for('index'))
