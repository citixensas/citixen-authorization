from django.http import JsonResponse


class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True

    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message

    def to_dict(self):
        return {'errorMessage': self.error_message}


class InvalidUsage(BaseCustomException):
    status_code = 400


class PermissionDenied(BaseCustomException):
    status_code = 403


def is_registered(exception):
    return isinstance(exception, BaseCustomException)


def process_exception(exception):
    if is_registered(exception):
        status = exception.status_code
        exception_dict = exception.to_dict()
    else:
        status = 500
        exception_dict = {'errorMessage': 'Unexpected Error!'}

    return JsonResponse(exception_dict, status=status)
