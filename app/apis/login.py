import os
import requests
import json

from flask import request, redirect
from flask_restx import Resource, Namespace
from flask_login import login_user
from oauthlib.oauth2 import WebApplicationClient

from extensions import db
from models.user import User

ns = Namespace(
    'login',
)


def get_google_provider_cfg():
    return requests.get('https://accounts.google.com/.well-known/openid-configuration').json()


def get_client():
    return WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))


@ns.route('')
class Login(Resource):
    def get(self):
        client = get_client()
        google_provider_cfg = get_google_provider_cfg()
        request_uri = client.prepare_request_uri(
            google_provider_cfg['authorization_endpoint'],
            redirect_uri=request.base_url + '/callback',
            scope=['openid', 'email', 'profile'],
        )
        return redirect(request_uri)


@ns.route('/callback')
class LoginCallback(Resource):
    def get(self):
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg['token_endpoint']

        client = get_client()
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=request.args.get('code')
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(
                os.getenv('GOOGLE_CLIENT_ID'),
                os.getenv('GOOGLE_CLIENT_SECRET')
            ),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if not userinfo_response.json().get('email_verified'):
            return 'User email not available or not verified by Google.', 400

        rj = userinfo_response.json()

        user = User.query.get_user(rj['sub'])
        if not user:
            user = User(
                google_user_id=rj['sub'],
                email=rj['email'],
                profile_pic=rj['picture'],
                name=rj['given_name']
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)

        return redirect('/')
