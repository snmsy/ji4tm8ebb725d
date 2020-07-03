import os
import requests

from oauthlib.oauth2 import WebApplicationClient

from models.user import User


def load_user(user_id):
    user = User.query.filter_by(google_user_id=user_id).first()
    if user:
        return user
    return None


def get_google_provider_cfg():
    return requests.get('https://accounts.google.com/.well-known/openid-configuration').json()


def get_client():
    return WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))
