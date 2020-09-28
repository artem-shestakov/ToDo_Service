from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from todo.users.models import User
from todo.board.models import Board, BoardSchema
from todo.api.utils.response import response_with
from todo.api.utils.decorators import exception
import todo.api.utils.response_code as response_code

boards_blueprint = Blueprint(
    "boards",
    __name__,
    url_prefix='/api/boards'
)


@boards_blueprint.route('/', methods=['GET'])
@exception
@jwt_required
def get_all_boards():
    """Get all user's boards"""
    user = User.objects(email=get_jwt_identity()).get()
    boards = Board.objects(user=user).all()
    board_schema = BoardSchema(many=True, only=['id', 'title', 'lists'])
    boards = board_schema.dump(boards)
    return response_with(response_code.SUCCESS_200, value={'boards': boards})


@boards_blueprint.route('/<board_id>', methods=['GET'])
@exception
def get_board_by_id(board_id):
    """
    Get board by ID
    :param board_id: The ID of board
    """
    board = Board.objects(id=board_id).get()
    board_schema = BoardSchema(only=['id', 'title', 'lists'])
    board = board_schema.dump(board)
    return response_with(response_code.SUCCESS_200, value={'boards': board})


@boards_blueprint.route('/', methods=['POST'])
@exception
@jwt_required
def create_board():
    """Create board"""
    data = request.get_json()
    if data:
        user = User.objects(email=get_jwt_identity()).get()
        board = Board(title=data['title'], user=user)
        board.save()
        board_schema = BoardSchema(only=['id', 'title', 'user'])
        board = board_schema.dump(board)
        return response_with(response_code.SUCCESS_201, value={'board': board})
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')


@boards_blueprint.route('/<board_id>', methods=['PUT'])
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


@boards_blueprint.route('/<board_id>', methods=['DELETE'])
@exception
def delete_board(board_id):
    """
    Delete user
    :param board_id: The ID of board
    """
    board = Board.objects(id=board_id).get()
    board.delete()
    return response_with(response_code.SUCCESS_201)
