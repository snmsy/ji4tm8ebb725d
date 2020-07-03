import os

from flask import Flask
from flask_restx import Api

from extensions import db, login_manager
from auth import load_user


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    api = Api(
        app=app,
        title='ji4tm8ebb725d',
        authorizations={
            'google': {
                'type': 'oauth2',
                'description': 'Google OAuth',
                'flow': 'accessCode',
                'tokenUrl': 'https://oauth2.googleapis.com/token',
                'authorizationUrl': 'https://accounts.google.com/o/oauth2/v2/auth',
                'scopes': {
                }
            }
        },
        security=['google']
    )

    from apis.login import ns as login_ns
    api.add_namespace(login_ns)
    from apis.logout import ns as logout_ns
    api.add_namespace(logout_ns)

    db.create_all(app=app)

    return app
