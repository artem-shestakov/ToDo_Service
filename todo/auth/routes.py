from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from todo.users.models import User
from todo.utils.decorators import exception
from todo.utils.response import response_with
import todo.utils.response_code as response_code

auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='../templates/auth'
)


@auth_blueprint.route('/login', methods=['POST'])
@exception
def login():
    data = request.get_json()
    if data:
        user = User.objects(email=data['email']).get()
        if not user:
            return response_with(response_code.UNAUTHORIZED_401, message='Invalid email or password')
        if user and not user.is_verified:
            return response_with(response_code.BAD_REQUEST_400, message='Please confirm your email')
        if user.verify_password(data['password'], user.password):
            access_token = create_access_token(identity=user.email)
            return response_with(response_code.SUCCESS_200, value={'message': f'Logged in as {user.email}',
                                                                   'access_token': access_token})
        else:
            return response_with(response_code.UNAUTHORIZED_401, message='Invalid email or password')
    else:
        return response_with(response_code.MISSING_PARAMETERS_422, message='Could not get JSON or JSON empty')
