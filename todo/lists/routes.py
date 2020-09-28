from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from todo.board.models import Board
from .models import List, ListSchema
from todo.api.utils.response import response_with
from todo.api.utils.decorators import exception
import todo.api.utils.response_code as response_code

lists_blueprint = Blueprint(
    'lists',
    __name__,
    url_prefix='/api/lists'
)


@lists_blueprint.route('/<id>', methods=['GET'])
@exception
@jwt_required
def get_all_lists(id):
    """
    Get all lists's
    :param id: List ID
    """
    getted_list = List.objects(id=id).get()
    list_schema = ListSchema()
    getted_list = list_schema.dump(getted_list)
    return response_with(response_code.SUCCESS_200, value={'list': getted_list})


@lists_blueprint.route('/', methods=['POST'])
@exception
@jwt_required
def create_list():
    """
    Create list of board
    """
    data = request.get_json()
    if data:
        new_list = List(title=data['title'])
        new_list.save()
        board = Board.objects(id=data['id_board']).get()
        board.lists.append(new_list)
        board.save()
        list_schema = ListSchema()
        new_list = list_schema.dump(new_list)
        return response_with(response_code.SUCCESS_201, value={'list': new_list})
    else:
        return response_with(response_code.BAD_REQUEST_400, message='Could not get JSON or JSON empty')