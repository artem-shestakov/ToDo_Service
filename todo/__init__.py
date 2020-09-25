from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from todo.api.utils.response import response_with
import todo.api.utils.response_code as response_code
import logging

# Init MongoDB object
mongo = MongoEngine()


def create_app(config_object):
    """
    Create Flask application object with all modules

    :param config_object: Configure object from config file
    """
    from .api import create_module as api_create_module
    from .board import create_module as board_create_module
    from .auth import create_module as auth_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    jwt = JWTManager(app)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(response_code.NOT_FOUND_404)

    @app.errorhandler(500)
    def not_found(e):
        logging.error(e)
        return response_with(response_code.SERVER_ERROR_500)

    mongo.init_app(app)

    # Register Blueprints
    api_create_module(app)
    auth_create_module(app)
    board_create_module(app)

    return app
