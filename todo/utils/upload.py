ALLOWED_EXTENSIONS = set(['image/jpeg', 'image/png'])


def allowed_file(file):
    """
    Verify file before upload

    :param file: Uploading file
    :return: Boolean
    """
    return '.' in file.filename and file.mimetype in ALLOWED_EXTENSIONS
