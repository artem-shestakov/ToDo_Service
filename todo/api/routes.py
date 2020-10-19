from flask import Blueprint, request, url_for
from flask_swagger_ui import get_swaggerui_blueprint

# URL to swagger UI page
SWAGGER_URL = '/api/docs'
#
API_URL = '/static/artem-shestakov-ToDo-0.1-resolved.json'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
