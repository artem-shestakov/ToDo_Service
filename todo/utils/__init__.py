def create_module(app):
    """
    Register Blueprint for utils API
    :param app: Flask application object
    """
    from .routes import utils_blueprint
    app.register_blueprint(utils_blueprint)
