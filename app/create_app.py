import os

from flask import Flask
from flask_restx import Api

from extensions import db, login_manager
from apis.login import ns as login_ns


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    # login_manager.init_app(app)

    api = Api(
        app=app,
        title='ji4tm8ebb725d',
        authorizations={
            'google': {
                'type': 'oauth2',
                'description': 'Google OAuth',
                'flow': 'accessCode',
                'tokenUrl': 'https://somewhere.com/token',
                'authorizationUrl': 'https://somewhere.com/auth',
                'scopes': {
                }
            }
        },
        security=['google']
    )
    api.add_namespace(login_ns)

    db.create_all(app=app)

    return app
