from .response import response_with
from functools import wraps, update_wrapper
from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError, FieldDoesNotExist
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
import todo.api.utils.response_code as response_code
from todo.users.models import User, Role
from flask_jwt_extended import get_jwt_identity


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
        except NotUniqueError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
        except DuplicateKeyError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
        except ServerSelectionTimeoutError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
        except ValueError as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
        except FieldDoesNotExist as err:
            return response_with(response_code.SERVER_ERROR_500, message=err)
    return wrapper_func


def has_role(roles):
    def wrapper(f):
        def wrapper_func(*args, **kwargs):
            user = User.objects(email=get_jwt_identity()).get()
            for role in roles:
                role = Role.objects(title=role).get()
                if role in user.roles:
                    return f(*args, **kwargs)
            return response_with(response_code.FORBIDDEN_403, message='Access denied')
        return update_wrapper(wrapper_func, f)
    return wrapper
