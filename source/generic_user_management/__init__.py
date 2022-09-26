from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from generic_user_management.generic_user_management_api import create_api
from os import path
import os

db = SQLAlchemy()
DB_NAME = "database/user_database.db"


def create_database(app):
    if not path.exists('generic_user_management/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


def create_app():
    app = Flask(__name__)
    secret_key = os.getenv('SECRET_KEY')
    if secret_key == 'None':
        secret_key = 'abc098def'

    app.config['SECRET_KEY'] = secret_key
    api = create_api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    create_database(app)

    # from .models import User, Note

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    return app
