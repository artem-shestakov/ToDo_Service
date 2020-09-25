from flask import Blueprint, make_response, jsonify, request
from todo.board.models import Board, BoardSchema
from todo.auth.models import User
from todo.api.utils.response import response_with
import todo.api.utils.response_code as code

board_blueprint = Blueprint(
    "board",
    __name__,
    url_prefix='/board'
)
