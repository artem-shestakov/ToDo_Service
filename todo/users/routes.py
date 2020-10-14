from flask import Blueprint, request, render_template, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
from todo.utils.decorators import exception, has_role
from todo.utils.response import response_with
from todo.utils.token import generate_verification_token, confirm_verification_token
from todo.utils.email import send_email
from todo.utils.upload import allowed_file
import todo.utils.response_code as response_code
from flask_jwt_extended import jwt_required
from .models import User, UserSchema, Role
from todo.board.models import Board, BoardSchema
import base64
import os

# Users API Blueprint
users_blueprint = Blueprint(
    'users',
    __name__,
    url_prefix='/api/users',
    template_folder='/auth'
)


@users_blueprint.route('/', methods=['GET'])
@exception
@jwt_required
@has_role(['administrator'])
def get_users():
    """Getting all users"""
    users = User.objects.all()
    users_schema = UserSchema(many=True, exclude=['password'])
    users = users_schema.dump(users)
    return response_with(response_code.SUCCESS_200, value={'users': users})


@users_blueprint.route('/', methods=['POST'])
@exception
def create_user():
    """Create user by POST request and send email confirmation"""
    data = request.get_json()
    if data:
        user_schema = UserSchema()
        data['password'] = User.generate_password(data['password'])
        user = user_schema.load(data)
        role = Role.objects(title='user').get()
        user.roles.append(role)
        user.save()

        # Generate email confirmation token and sent it to user
        token = generate_verification_token(data['email'])
        logo = base64.b64encode(open("./todo/static/images/logo.png", "rb").read()).decode()
        html = render_template('email_confirmation.html', logo=logo, token=token)
        subject = "Please verify your email"
        send_email.apply_async(args=(user.email, subject, html))

        # Get this user information for response
        user_schema = UserSchema(exclude=['password'])
        user = user_schema.dump(user)
        return response_with(response_code.SUCCESS_201, value={'user': user})
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@users_blueprint.route('/<user_id>', methods=['GET'])
@exception
@jwt_required
def get_user_by_id(user_id):
    """
    Getting user's info by ID

    :param user_id: User's ID
    """
    user = User.objects(id=user_id).get()
    boards = Board.objects(user=user).all()
    user_schema = UserSchema(exclude=['password'])
    user = user_schema.dump(user)
    board_schema = BoardSchema(many=True, only=['id', 'title'])
    boards = board_schema.dump(boards)
    user['boards'] = boards
    return response_with(response_code.SUCCESS_200, value={'user': user})


@users_blueprint.route('/<user_id>', methods=['PUT'])
@exception
@jwt_required
def update_user(user_id):
    """
    Update user's attributes

    :param user_id: User's ID
    """
    data = request.get_json()
    if data:
        user = User.objects(id=user_id).get()
        if data.get('email') or data.get('first_name') or data.get('last_name'):
            if data.get('email'):
                user.update(email=data['email'])
            if data.get('first_name'):
                user.update(first_name=data['first_name'])
            if data.get('last_name'):
                user.update(last_name=data['last_name'])
            user = User.objects(id=user_id).get()
            user_schema = UserSchema(exclude=['password'])
            user = user_schema.dump(user)
            return response_with(response_code.SUCCESS_201, value={'user': user})
        else:
            return response_with(response_code.MISSING_PARAMETERS_422, message='Check you JSON request')
    else:
        return response_with(response_code.MISSING_PARAMETERS_422, message='Could not get JSON or JSON empty')


@users_blueprint.route('/<user_id>', methods=['DELETE'])
@exception
@jwt_required
@has_role(['administrator'])
def delete_user(user_id):
    """
    Delete user

    :param user_id: User's ID
    """
    user = User.objects(id=user_id).get()
    user.delete()
    return response_with(response_code.SUCCESS_201)


@users_blueprint.route('/confirm/<verification_token>', methods=['GET'])
@exception
def user_verification(verification_token):
    """
    Verify user's email

    :param verification_token: Token for confirmation email
    """
    email = confirm_verification_token(verification_token)
    user = User.objects(email=email).get()
    if user.is_verified:
        response_with(response_code.INVALID_INPUT_422)
    else:
        user.update(is_verified=True)
        return response_with(response_code.SUCCESS_200, value={'message': 'Email verified, you can proceed login now'})


@users_blueprint.route('/<user_id>/avatar', methods=['POST'])
@exception
@jwt_required
def set_user_avatar(user_id):
    """
    Upload user's avatar

    :param user_id: User ID
    """
    file = request.files['avatar']
    user = User.objects(id=user_id).get()
    if file and allowed_file(file):
        filename = secure_filename(file.filename)
        filename = str(user.id) + os.path.splitext(filename)[1]
        file.save(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}{filename}")
        user.avatar = filename
        user.save()
        user_schema = UserSchema(exclude=['password'])
        user = user_schema.dump(user)
        return response_with(response_code.SUCCESS_201, value={'user': user})
    else:
        return response_with(response_code.INVALID_INPUT_422,
                             message='No image in request or image format is not accepted')


@users_blueprint.route('/<user_id>/avatar', methods=['GET'])
@exception
def uploaded_file(user_id):
    """
    Getting user's avatar

    :param user_id: User ID
    :return: Avatar image
    """
    user = User.objects(id=user_id).get()
    if user.avatar:
        return send_from_directory(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}", user.avatar)
    else:
        return response_with(response_code.NOT_FOUND_404)
