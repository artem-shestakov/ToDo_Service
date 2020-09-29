def create_model(app):
    """
    Register Blueprint for Users API
    :param app: Flask application object
    """
    from .routes import users_blueprint
    app.register_blueprint(users_blueprint)
