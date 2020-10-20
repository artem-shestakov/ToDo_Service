from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from todo.utils.response import response_with
import todo.utils.response_code as response_code
from celery import Celery
import logging

# Init MongoDB object
mongo = MongoEngine()

# Init Flask-Mail object
mail = Mail()

# Init Celery object
celery = Celery(__name__)


def init_celery(app, celery):
    """
    Update celery config and celery object with application context

    :param app: Flask application object
    :param celery: Celery object
    """
    celery.conf.update(broker_url=app.config['CELERY_BROKER_URL'],
                       result_backend=app.config['CELERY_RESULT_BACKEND'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


def create_app(config_object):
    """
    Create Flask application object with all modules

    :param config_object: Configure object from config file
    """
    from .api import create_module as api_create_module
    from .users import create_model as users_create_module
    from .board import create_module as board_create_module
    from .lists import create_module as lists_create_module
    from .auth import create_module as auth_create_module
    from .utils import create_module as utils_create_module

    app = Flask(__name__)
    app.config.from_object(config_object)

    jwt = JWTManager(app)

    @app.errorhandler(401)
    def not_found(e):
        logging.error(e)
        return response_with(response_code.UNAUTHORIZED_401)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(response_code.NOT_FOUND_404)

    @app.errorhandler(500)
    def not_found(e):
        logging.error(e)
        return response_with(response_code.SERVER_ERROR_500)

    mongo.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    api_create_module(app)
    users_create_module(app)
    auth_create_module(app)
    board_create_module(app)
    lists_create_module(app)
    utils_create_module(app)

    return app
