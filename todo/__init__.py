from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from todo.utils.response import response_with
import todo.utils.response_code as response_code
# from celery import Celery
from flask_celery import Celery as Celery_app
import logging

# Init MongoDB object
mongo = MongoEngine()
celery_app = Celery_app()
mail = Mail()


# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery


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
    mail.init_app(app)
    celery_app.init_app(app)

    # Register Blueprints
    api_create_module(app)
    users_create_module(app)
    auth_create_module(app)
    board_create_module(app)
    lists_create_module(app)

    return app
