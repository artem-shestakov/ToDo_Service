from flask import Blueprint, request
from todo.auth.models import User, UserSchema
from todo.utils.response import response_with
import todo.utils.response_code as response_code
from mongoengine.errors import ValidationError, DoesNotExist
from pymongo.errors import ServerSelectionTimeoutError

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/user/all', methods=['GET'])
def get_users():
    """Getting all users"""
    try:
        users = User.objects.all()
        users_schema = UserSchema(many=True, only=['id', 'email', 'first_name', 'last_name'])
        users = users_schema.dump(users)
        return response_with(response_code.SUCCESS_200, value={'users': users})
    except ServerSelectionTimeoutError as err:
        return response_with(response_code.SERVER_ERROR_500, message=err)


@api_blueprint.route('/user/create', methods=['POST'])
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
        except ServerSelectionTimeoutError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
    else:
        return response_with(response_code.BAD_REQUEST_400)


@api_blueprint.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Getting user's info by ID"""
    try:
        user = User.objects(id=user_id).get()
        user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
        user = user_schema.dump(user)
        return response_with(response_code.SUCCESS_200, value={'user': user})
    except ValidationError as err:
        return response_with(response_code.BAD_REQUEST_400, message=err)
    except DoesNotExist as err:
        return response_with(response_code.NOT_FOUND_404, message=err)
    except ServerSelectionTimeoutError as err:
        return response_with(response_code.SERVER_ERROR_500, message=err)