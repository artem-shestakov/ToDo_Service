from flask import Blueprint, send_from_directory, current_app


utils_blueprint = Blueprint(
    'utils',
    __name__,
    url_prefix='/'
)


@utils_blueprint.route('/avatar/')
def uploaded_file():
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], 'avatar.png')
