from flask import Blueprint, request

# Blueprint init
api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/ap'
)
