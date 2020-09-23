def create_module(app, **kwargs):
    """
    Register Blueprint

    :param app: Flask application object
    """
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)
