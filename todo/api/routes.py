from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from todo.auth.models import User, UserSchema
from todo.board.models import Board, BoardSchema
from todo.api.utils.response import response_with
from todo.api.utils.decorators import exception
import todo.api.utils.response_code as response_code

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/user', methods=['GET'])
@exception
@jwt_required
def get_users():
    """Getting all users"""
    users = User.objects.all()
    users_schema = UserSchema(many=True, only=['id', 'email', 'first_name', 'last_name', 'created'])
    users = users_schema.dump(users)
    return response_with(response_code.SUCCESS_200, value={'users': users})


@api_blueprint.route('/user', methods=['POST'])
@exception
def create_user():
    """Create user by POST request"""
    data = request.get_json()
    if data:
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.password = User.generate_password(data['password'])
        user.save()
        # Get this user information for response
        user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
        user = user_schema.dump(user)
        return response_with(response_code.SUCCESS_201, value={'user': user})
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@api_blueprint.route('/user/<user_id>', methods=['GET'])
@exception
def get_user_by_id(user_id):
    """
    Getting user's info by ID
    :param user_id: User's ID
    """
    user = User.objects(id=user_id).get()
    boards = Board.objects(user=user).all()
    user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
    user = user_schema.dump(user)
    board_schema = BoardSchema(many=True, only=['id', 'name'])
    boards = board_schema.dump(boards)
    user['boards'] = boards
    return response_with(response_code.SUCCESS_200, value={'user': user})


@api_blueprint.route('/user/<user_id>', methods=['PUT'])
@exception
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
            user_schema = UserSchema(only=['email', 'first_name', 'last_name'])
            user = user_schema.dump(user)
            return response_with(response_code.SUCCESS_201, value={'user': user})
        else:
            return response_with(response_code.MISSING_PARAMETERS_422, message='Check you JSON request')
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@api_blueprint.route('/user/<user_id>', methods=['DELETE'])
@exception
def delete_user(user_id):
    """
    Delete user
    :param user_id: User's ID
    """
    user = User.objects(id=user_id).get()
    user.delete()
    return response_with(response_code.SUCCESS_201)


@api_blueprint.route('/board', methods=['GET'])
@exception
@jwt_required
def get_all_boards():
    """Get all user's boards"""
    user = User.objects(email=get_jwt_identity()).get()
    boards = Board.objects(user=user).all()
    board_schema = BoardSchema(many=True, only=['id', 'title'])
    boards = board_schema.dump(boards)
    return response_with(response_code.SUCCESS_200, value={'boards': boards})


@api_blueprint.route('/board/<board_id>', methods=['GET'])
@exception
def get_board_by_id(board_id):
    """
    Get board by ID
    :param board_id: The ID of board
    """
    board = Board.objects(id=board_id).get()
    board_schema = BoardSchema(only=['id', 'title', 'user'])
    board = board_schema.dump(board)
    return response_with(response_code.SUCCESS_200, value={'boards': board})


@api_blueprint.route('/board', methods=['POST'])
@exception
def create_board():
    """Create board"""
    data = request.get_json()
    if data:
        user = User.objects(id=data['user_id']).get()
        board = Board(title=data['title'], user=user)
        board.save()
        board_schema = BoardSchema(only=['id', 'title', 'user'])
        board = board_schema.dump(board)
        return response_with(response_code.SUCCESS_201, value={'board': board})
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@api_blueprint.route('/board/<board_id>', methods=['PUT'])
@exception
def update_board(board_id):
    data = request.get_json()
    if data:
        board = Board.objects(id=board_id).get()
        if data.get('title'):
            if data.get('title'):
                board.update(title=data['title'])
            board = Board.objects(id=board_id).get()
            board_schema = BoardSchema(only=['id', 'title', 'user'])
            board = board_schema.dump(board)
            return response_with(response_code.SUCCESS_201, value={'board': board})
        else:
            return response_with(response_code.MISSING_PARAMETERS_422, message='Check you JSON request')
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@api_blueprint.route('/board/<board_id>', methods=['DELETE'])
@exception
def delete_board(board_id):
    """
    Delete user
    :param board_id: The ID of board
    """
    board = Board.objects(id=board_id).get()
    board.delete()
    return response_with(response_code.SUCCESS_201)
