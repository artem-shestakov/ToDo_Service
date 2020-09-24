from flask import Blueprint, request, make_response, jsonify
from .models import User, UserSchema
from todo.utils.response import response_with
from mongoengine.errors import ValidationError, DoesNotExist
import todo.utils.response_code as response_code


auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/api/auth'
)


@auth_blueprint.route('/users', methods=['GET'])
def get_users():
    """Getting all users"""
    users = User.objects.all()
    users_schema = UserSchema(many=True, only=['id', 'email', 'first_name', 'last_name'])
    users = users_schema.dump(users)
    return response_with(response_code.SUCCESS_200, value={'users': users})


@auth_blueprint.route('/user/create', methods=['POST'])
def create_user():
    """Create user by POST request"""
    data = request.get_json()
    if data:
        try:
            user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
            user.save()
            # Get this user information for response
            user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
            user = user_schema.dump(user)
            return response_with(response_code.SUCCESS_201, value={'user': user})
        except KeyError as err:
            return response_with(response_code.MISSING_PARAMETERS_422, message=err)
    else:
        return response_with(response_code.BAD_REQUEST_400)


@auth_blueprint.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Getting user's info by ID"""
    try:
        user = User.objects(id=user_id).get()
    except ValidationError as err:
        return response_with(response_code.BAD_REQUEST_400, message=err)
    except DoesNotExist as err:
        return response_with(response_code.NOT_FOUND_404, message=err)
    user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
    user = user_schema.dump(user)
    return response_with(response_code.SUCCESS_200, value={'user': user})
