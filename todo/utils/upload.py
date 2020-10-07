import filetype

allowed_extension = set(['image/jpeg', 'image/png', 'jpeg'])


def allowed_file(filename):
    """
    Verify file before upload
    :param filename: Uploading file
    :return: Boolean
    """
    return filetype in allowed_extension
