from flask import make_response, jsonify


def response_with(response, headers={}, value=None, message=None):
    """
    Send standard response for request
    :param response: Dict with messae and response code
    :param headers: Response header
    :param value: Additional information about objects
    :param message: Additional text message
    :return: JSON response
    """
    result = {}
    if value is not None:
        result.update(value)
    if response.get('message', None) is not None:
        result.update({'message': response['message'] + f' {message}'})
    result.update({'code': response['code']})
    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'Server': 'ToDo REST API server'})
    return make_response(jsonify(result), response['http_code'], headers)
