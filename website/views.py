from flask import current_app, Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import User
from . import mongo
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

"""This file contains non authentication routes for the website.
The 'request' object is used to access the data sent by the user.
The 'User' object allows us to store users and access their data.
The 'current_user' is a User object that represents the current user.
The 'flash' method is used to display messages to the user.
flask_login is used to handle the user session and access control.
"""

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# login_required decorator is used to prevent unauthenticated users from accessing the home page.
@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/profile',  methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)