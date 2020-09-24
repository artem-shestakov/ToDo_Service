from flask import Flask
from flask_mongoengine import MongoEngine

# Init MongoDB object
mongo = MongoEngine()


def create_app(config_object):
    """
    Create Flask application object with all modules

    :param config_object: Configure object from config file
    """
    from .board import create_module as board_create_module
    from .auth import create_module as auth_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    mongo.init_app(app)

    # Register Blueprints
    auth_create_module(app)
    board_create_module(app)

    return app
