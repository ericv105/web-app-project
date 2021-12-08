from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

mongo = None


def create_app():
    """Used to create the flask app and connect to the database
    app is the flask app that gets returned
    mongo is used to connect to the database
    login_manager is used to manage the login process
    load_user is used to load the user from the database
    """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'changethiskeylater'
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://mongo:27017/test_database'}
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    app.config['AVATAR_FOLDER'] = 'static/avatars/'

    global mongo
    mongo = MongoEngine(app)

    from .views import views
    from .auth import auth
    from .message import message

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(message, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

    return app
