from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
def index():
	title = "Flask Foundation"
	head = "Welcome to Billy's Flask Foundation!"
	return render_template("index.html",
		title = title,
		head = head)