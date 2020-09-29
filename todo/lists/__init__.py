def create_module(app):
    """
    Register Lists Blueprint
    :param app: Flask application object
    """
    from .routes import lists_blueprint
    app.register_blueprint(lists_blueprint)
