from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from .models import User, UserSchema
from todo.api.utils.decorators import exception
from todo.api.utils.response import response_with
import todo.api.utils.response_code as response_code

auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@auth_blueprint.route('/login', methods=['POST'])
@exception
def login():
    data = request.get_json()
    if data:
        user = User.objects(email=data['email']).get()
        if not user:
            return response_with(response_code.UNAUTHORIZED_401, message='Invalid email or password')
        if user.verify_password(data['password'], user.password):
            access_token = create_access_token(identity=user.email)
            return response_with(response_code.SUCCESS_201, value={'message': f'Logged in as {user.email}',
                                                                   'access_token': access_token})
        else:
            return response_with(response_code.UNAUTHORIZED_401, message='Invalid email or password')
    else:
        return response_with(response_code.MISSING_PARAMETERS_422, message='Could not get JSON or JSON empty')
