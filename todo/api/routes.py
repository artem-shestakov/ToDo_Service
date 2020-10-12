from flask import Blueprint, request, url_for
from flask_swagger_ui import get_swaggerui_blueprint

# Blueprint init
# api_blueprint = Blueprint(
#     'api',
#     __name__,
#     url_prefix='/api'
# )

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
