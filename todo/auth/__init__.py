def create_module(app):
    """
    Register Blueprint for auth module

    :param app: Flask application object
    """
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)
