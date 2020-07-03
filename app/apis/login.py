from flask_restx import Resource, Namespace

from models.user import User

ns = Namespace(
    'login',
)


@ns.route('/login')
class Login(Resource):
    def get(self):
        pass
