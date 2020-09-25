from flask import Blueprint, request, make_response, jsonify
from .models import User, UserSchema
from todo.utils.response import response_with
from mongoengine.errors import ValidationError, DoesNotExist
from pymongo.errors import ServerSelectionTimeoutError
import todo.utils.response_code as response_code


auth_blueprint = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)
