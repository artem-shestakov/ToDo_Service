from flask import Blueprint

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix='/api'
)


@api_blueprint.route('/')
def index():
    return 'Hello from API'