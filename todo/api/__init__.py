from flask_restful import Api
from .users.views import UserApi


def create_module(app, **kwargs):
    """Create Blueprint method for API"""
    from .routes import swagger_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    app.add_url_rule('/api/v1/users', view_func=UserApi.as_view('users'))
