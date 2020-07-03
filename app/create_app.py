import os

from flask import Flask
from flask_restx import Api

from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')

    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    api = Api(
        app=app,
        title='ji4tm8ebb725d'
    )

    from apis.login import ns as login_ns
    api.add_namespace(login_ns)
    from apis.logout import ns as logout_ns
    api.add_namespace(logout_ns)

    return app


def load_user(user_id):
    from models.user import User
    return User.query.get_user(user_id)
