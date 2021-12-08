from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
import bcrypt
from .auth import current_users
from .auth import current_messages

"""This file contains the authentication routes for the website.
The 'request' object is used to access the data sent by the user.
The 'User' object allows us to store users and access their data.
The 'current_user' is a User object that represents the current user.
The 'flash' method is used to display messages to the user.
flask_login is used to handle the user session and access control.
"""

message = Blueprint('message', __name__)

@message.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():

    if request.method == 'POST':
        data = request.form
        username = data['username']
        message = data['message']
        url = current_user.username + username
        hash =  bcrypt.hashpw(
            url.encode(), bcrypt.gensalt()).decode()
        current_messages['/messages/' + hash] = message + '\n'
        flash('Message Sent!', category='success')
        return redirect('/messages/' + hash)


    active_users = ''
    for i in current_users:
        if i != current_user.username:
            active_users +=  i + '\n'
    
    return render_template('dm.html', user=current_user, USERS = active_users)
"""
for i in auth.current_messages.keys():
    @auth.route(i, methods=['GET', 'POST'])
    @login_required
    def reply():
        if request.method == 'POST':
            data = request.form
            reply = data['reply']
            #current_messages[i] += 
        return render_template('dm.html', user=current_user)
"""