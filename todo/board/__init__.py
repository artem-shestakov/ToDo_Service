def create_module(app, **kwargs):
    """
    Register Blueprint for boards, columns and cards

    :param app: Flask application object
    """
    from todo.board.routes import board_blueprint
    app.register_blueprint(board_blueprint)
