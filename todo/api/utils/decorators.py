from .response import response_with
from functools import wraps
from mongoengine.errors import ValidationError, DoesNotExist
from pymongo.errors import ServerSelectionTimeoutError
import todo.api.utils.response_code as response_code


def exception(f):
    """Decorator for catching exceptions"""
    @wraps(f)
    def wrapper_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as err:
            return response_with(response_code.MISSING_PARAMETERS_422, message=err)
        except ValidationError as err:
            return response_with(response_code.BAD_REQUEST_400, message=err)
        except DoesNotExist as err:
            return response_with(response_code.NOT_FOUND_404, message=err)
        except ServerSelectionTimeoutError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
    return wrapper_func
