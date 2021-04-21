import logging
import traceback

from flask import request, jsonify
from flask_restplus import Api, Resource, reqparse, fields
from scratch import settings
from scratch.database.models import Users
from sqlalchemy.orm.exc import NoResultFound
from scratch.api.utils import save_to_db, create_response
from scratch.database import db

log = logging.getLogger(__name__)

api = Api(version='1.0.0', title='User API',
          description='A Very Simple User API')
ns = api.namespace('users', description='Users Apis')


pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument(
    'page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')

user_fields = api.model('User', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True),
})

user_list_fields = api.model('UserList', {
    "Users": fields.List(fields.Nested(user_fields)),
})

user_id = api.model('User id', {
    'id': fields.Integer(required=True, description='ID of the User to Fetch', minimum=1)
})


@ns.route('/')
class User(Resource):
    @api.doc(params={'page': {"type": "int", "required": False, "default": "1", "help": "Page number"},
                     "per_page": {"type": "int", "required": False, "default": "10", "help": "results per page",
                                  "choices": [2, 10, 20, 30, 40, 50]}})
    # @api.expect(pagination_arguments)
    @api.response(200, 'OK', user_list_fields)
    @api.doc(description='Returns a List of Users.')
    def get(self):
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        users_query = db.session.query(Users)
        users_page = users_query.paginate(page, per_page, error_out=False)
        result = [create_response(user) for user in users_page.items]
        return jsonify({"Users": result})

    @api.response(200, 'OK', user_fields)
    @api.doc(description='Creates a New User')
    @api.expect(user_fields)
    def post(self):
        name = request.json.get('name')
        user = Users(None, name)
        save_to_db(user)
        return jsonify(create_response(user))
        
        
@ns.route('/<int:id>')
@api.response(404, 'User not found.')
class UserId(Resource):
    @api.response(200, 'OK')
    def get(self, id):
        user = db.session.query(Users).filter(Users.id == id).one()
        return jsonify(create_response(user))


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """No results found in database"""
    log.warning(traceback.format_exc())
    if not settings.FLASK_DEBUG:
        return {'message': 'A database result was required but none was found.'}, 404
