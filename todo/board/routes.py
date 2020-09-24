from flask import Blueprint, make_response, jsonify, request
from todo.board.models import Board, BoardSchema
from todo.auth.models import User, UserSchema

board_blueprint = Blueprint(
    "board",
    __name__,
    url_prefix='/api/board'
)


@board_blueprint.route('/all', methods=['GET'])
def get_all_boards():
    """Get all boards"""
    boards = Board.objects.all()
    board_schema = BoardSchema(many=True, only=['id', 'name', 'user'])
    boards = board_schema.dump(boards)
    return make_response(jsonify({'boards': boards}))


@board_blueprint.route('/', methods=['POST'])
def create_board():
    """Create board"""
    data = request.get_json()
    board = Board(name=data['name'])
    board.save()
    board_schema = BoardSchema(only=['name'])
    board = board_schema.dump(board)
    return make_response(jsonify({'board': board}), 201)
