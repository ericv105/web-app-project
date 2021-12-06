from flask import Flask
import pymongo

client = pymongo.MongoClient('mongo')
db = client.test_database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'changethiskeylater'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app