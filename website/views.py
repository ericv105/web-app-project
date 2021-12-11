
from flask import current_app, Blueprint, render_template, request, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Upload
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
    uploads = Upload.objects()
    return render_template('home.html', user=current_user, uploads=uploads)
  
@views.route('/static/uploads/<name>')
def download_file(name):
    return send_from_directory(directory=current_app.config["UPLOAD_FOLDER"], path=name)
  
@views.route('/profile',  methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(current_user.username + '.' + ext)
            file_path = os.path.join(current_app.config['AVATAR_FOLDER'], filename)
            
            current_user.avatar_path = file_path
            current_user.save()

            file.save(os.path.join(current_app.root_path, file_path))
    return render_template('profile.html', user=current_user)
