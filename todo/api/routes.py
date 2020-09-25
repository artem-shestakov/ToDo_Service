from flask import Blueprint, request, current_app
from todo.auth.models import User, UserSchema
from todo.utils.response import response_with
from todo.utils.decorators import exception
import todo.utils.response_code as response_code

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/user/all', methods=['GET'])
@exception
def get_users():
    """Getting all users"""
    users = User.objects.all()
    users_schema = UserSchema(many=True, only=['id', 'email', 'first_name', 'last_name'])
    users = users_schema.dump(users)
    return response_with(response_code.SUCCESS_200, value={'users': users})


@api_blueprint.route('/user/create', methods=['POST'])
@exception
def create_user():
    """Create user by POST request"""
    data = request.get_json()
    if data:
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.save()
        # Get this user information for response
        user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
        user = user_schema.dump(user)
        return response_with(response_code.SUCCESS_201, value={'user': user})
    else:
        return response_with(response_code.BAD_REQUEST_400)


@api_blueprint.route('/user/<user_id>', methods=['GET'])
@exception
def get_user_by_id(user_id):
    """Getting user's info by ID"""
    user = User.objects(id=user_id).get()
    user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
    user = user_schema.dump(user)
    return response_with(response_code.SUCCESS_200, value={'user': user})
