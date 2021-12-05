from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
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
        
    return render_template('register.html')