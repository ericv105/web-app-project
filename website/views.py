from flask import Blueprint, render_template, current_app, send_from_directory
# from werkzeug.utils import send_from_directory
from flask_login import login_required, current_user
from .models import User

"""This file contains non authentication routes for the website.
The 'request' object is used to access the data sent by the user.
The 'User' object allows us to store users and access their data.
The 'current_user' is a User object that represents the current user.
The 'flash' method is used to display messages to the user.
flask_login is used to handle the user session and access control.
"""

views = Blueprint('views', __name__)

# login_required decorator is used to prevent unauthenticated users from accessing the home page.
@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/static/uploads/<name>')
def download_file(name):
    return send_from_directory(directory=current_app.config["UPLOAD_FOLDER"], path=name)