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
		g.user = session['twitter']

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
	title = "Grov - A Work In Progress"
	head = "THIS IS GROV"
	return render_template("index.html",
		title = title,
		head = head)

@app.route('/login')
def login():
	return twitter.authorize(callback=url_for('auth', 
		next=request.args.get('next') or request.referrer or None))

@app.route('/auth')
@twitter.authorized_handler
def auth(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None:
		flash(u"You've been denied access.")
		return redirect(next_url)
	else:
		session['twitter'] = resp
	return redirect(next_url)

@app.route('/logout')
def logout():
	session.pop('twitter', None)
	return redirect(url_for('index'))
