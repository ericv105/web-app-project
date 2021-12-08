from flask_login import UserMixin
from . import mongo

"""Here are the models for the database
Currently, only the User model is implemented
We will add more models as we go along like a Post model


To query the users by username, we will use the following syntax: user = User.objects(username='username').first()
This will return the first user with the username 'username'

To query the users by online status, we will use the following syntax: user = User.objects(online=True)
This will return all users that are online

To save the user to the database, we will use the following syntax: new_user = User(username='username', password='password', online=False).save()
This saves the user to the database in a dictionary format
"""


class User(mongo.Document, UserMixin):
    username = mongo.StringField(max_length=50)
    password = mongo.StringField(max_length=70)
    online = mongo.BooleanField(default=False)
    avatar_path = mongo.StringField(max_length=200)

# the filename contains the filename only not the path for the image
class Upload(mongo.Document):
    filename = mongo.StringField(max_length=100)
    votes = mongo.IntField(min_value=-100000, max_value=100000)
    file_path = mongo.StringField(max_length=300)
