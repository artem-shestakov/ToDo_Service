def create_module(app, **kwargs):
    """
    Register Blueprint for boards, lists and cards

    :param app: Flask application object
    """
    from todo.board.routes import boards_blueprint
    app.register_blueprint(boards_blueprint)
