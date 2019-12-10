from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True

    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message

    def to_dict(self):
        exception_dict = {
            'code': self.status_code,
            'status_code': self.status_code,
            'errors': [
                {
                    'field': 'non_field_errors',
                    'message': self.error_message
                }
            ]
        }
        return exception_dict


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
        exception_dict = {
            'code': status,
            'status_code': status,
            'errors': [
                {
                    'field': 'non_field_errors',
                    'message': _("The server could not understand your request.")
                }
            ]
        }

    return JsonResponse(exception_dict, status=status)
