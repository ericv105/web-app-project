from flask import current_app, Blueprint, render_template, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
import bcrypt

"""This file contains the authentication routes for the website.
The 'request' object is used to access the data sent by the user.
The 'User' object allows us to store users and access their data.
The 'current_user' is a User object that represents the current user.
The 'flash' method is used to display messages to the user.
flask_login is used to handle the user session and access control.
"""

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # use the request object to access data sent by the user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            # logs in the user and redirects to the home page
            # this updates current user accordingly
            login_user(user)
            flash('Logged in successfully!', category='success')
            return redirect('/')
        else:
            flash('Incorrect username or password.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect('/login')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # use the request object to access data sent by the user
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        confirm_password = data['confirm-password']

        # Queries the database to see if the username is already taken.
        user = User.objects(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters long.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif password != confirm_password:
            flash('Passwords must match.', category='error')
        else:
            # Hashes the password and stores the user in the database.
            password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            new_user = User(username=username,
                            password=password, online=False, avatar_path="static/uploads/default.png").save()
            flash('Successfully registered!', category='success')
            return redirect('/login')
    return render_template('register.html', user=current_user)
