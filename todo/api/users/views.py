from flask import request, render_template
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from todo.users.models import User, UserSchema, Role
from todo.board.models import Board, BoardSchema
from todo.utils.response import response_with
from todo.utils.token import generate_verification_token, confirm_verification_token
from todo.utils.email import send_email
from todo.utils.decorators import exception
import todo.utils.response_code as response_code
import base64


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