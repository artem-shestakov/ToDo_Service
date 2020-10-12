def create_module(app):
    """Create Blueprint method for API"""
    from .routes import swagger_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
