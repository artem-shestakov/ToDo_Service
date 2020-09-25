def create_module(app):
    """Create Blueprint method for API"""
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)
