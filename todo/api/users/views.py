from flask import request, render_template, send_from_directory, current_app, url_for
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from todo.users.models import User, UserSchema, Role
from todo.board.models import Board, BoardSchema
from todo.utils.response import response_with
from todo.utils.token import generate_verification_token, confirm_verification_token
from todo.utils.email import send_email
from todo.utils.decorators import exception
import todo.utils.response_code as response_code
from todo.utils.upload import allowed_file
import base64
import os
import hashlib


class UserApi(MethodView):
    @exception
    @jwt_required
    def get(self):
        """Getting user's profile"""
        user_email = get_jwt_identity()
        user = User.objects(email=user_email).get()
        boards = Board. objects(user=user).all()
        user_schema = UserSchema(exclude=['password'])
        user = user_schema.dump(user)
        board_schema = BoardSchema(many=True, exclude=['user', 'lists'])
        boards = board_schema.dump(boards)
        user['boards'] = boards
        return response_with(response_code.SUCCESS_200, value={'user': user})

    @exception
    def post(self):
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

    @exception
    @jwt_required
    def put(self):
        data = request.get_json()
        if data:
            user_email = get_jwt_identity()
            user = User.objects(email=user_email).get()
            if data.get('email') or data.get('first_name') or data.get('last_name'):
                if data.get('email'):
                    user.update(email=data['email'])
                if data.get('first_name'):
                    user.update(first_name=data['first_name'])
                if data.get('last_name'):
                    user.update(last_name=data['last_name'])
                user = User.objects(email=user_email).get()
                user_schema = UserSchema(exclude=['password'])
                user = user_schema.dump(user)
                return response_with(response_code.SUCCESS_201, value={'user': user})
            else:
                return response_with(response_code.MISSING_PARAMETERS_422, message='Check you JSON request')
        else:
            return response_with(response_code.MISSING_PARAMETERS_422, message='Could not get JSON or JSON empty')


class UserAvatarApi(MethodView):
    @jwt_required
    @exception
    def get(self):
        """
        Getting user's avatar

        :return: Avatar image
        """
        user_email = get_jwt_identity()
        user = User.objects(email=user_email).get()
        if user.avatar:
            return send_from_directory(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}", user.avatar)
        else:
            return response_with(response_code.NOT_FOUND_404)

    @jwt_required
    @exception
    def post(self):
        """Upload user's avatar"""
        file = request.files['avatar']
        user_email = get_jwt_identity()
        user = User.objects(email=user_email).get()
        if file and allowed_file(file):
            filename = hashlib.md5(user.email.lower().encode('utf-8')).hexdigest()
            file.save(f"{current_app.root_path}{current_app.config['UPLOAD_FOLDER']}{filename}")
            if current_app.config['AVATAR_SERVER']:
                user.avatar = current_app.config['AVATAR_SERVER'] + filename
            else:
                user.avatar = filename
            user.save()
            user_schema = UserSchema(exclude=['password'])
            user = user_schema.dump(user)
            return response_with(response_code.SUCCESS_201, value={'user': user})
        else:
            return response_with(response_code.INVALID_INPUT_422,
                                 message='No image in request or image format is not accepted')
