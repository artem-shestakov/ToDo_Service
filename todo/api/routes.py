from flask import Blueprint, make_response, jsonify, request
from todo.board.model import Board, BoardSchema

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/boards', methods=['GET'])
def index():
    boards = Board.objects.all()
    board_schema = BoardSchema(many=True, only=['id', 'name'])
    boards = board_schema.dump(boards)
    return make_response(jsonify({'boards': boards}))


@api_blueprint.route('/board', methods=['POST'])
def create_board():
    data = request.get_json()
    board = Board(name=data['name'])
    board.save()
    board_schema = BoardSchema(only=['name'])
    board = board_schema.dump(board)
    return make_response(jsonify({'board': board}), 201)
