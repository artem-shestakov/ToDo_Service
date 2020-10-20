from .users.views import UserApi, UserAvatarApi


def create_module(app, **kwargs):
    """Create Blueprint method for API"""
    from .routes import swagger_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # Users
    app.add_url_rule('/api/v1/users', view_func=UserApi.as_view('users'))
    app.add_url_rule('/api/v1/users/avatar', view_func=UserAvatarApi.as_view('avatars'))
