from flask import Blueprint, render_template, request, flash, redirect
from website import db
import bcrypt

collection = db.users
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode(), user['password']):
            flash('Logged in successfully!', category='success')
            return redirect('/')
        else:
            flash('Incorrect username or password.', category='error')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return 'logout'

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        confirm_password = data['confirm-password']

        if len(username) < 3:
            flash('Username must be at least 3 characters long.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif password != confirm_password:
            flash('Passwords must match.', category='error')
        else:
            flash('Successfully registered!', category='success')
            collection.insert_one({'username': username, 'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())})
        
    return render_template('register.html')