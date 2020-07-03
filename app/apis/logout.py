from flask import redirect, url_for
from flask_restx import Resource, Namespace
from flask_login import login_required, logout_user

ns = Namespace(
    'logout',
    decorators=[login_required]
)


@ns.route('')
class Logout(Resource):
    def get(self):
        logout_user()
        return redirect(url_for("index"))
