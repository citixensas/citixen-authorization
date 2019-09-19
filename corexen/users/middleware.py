from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.

    This will work with existing decorators like LoginRequired  ;)

    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user or AnonymousUser()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """
    def process_request(self, request):
        admin_url = '/%s' % settings.ADMIN_URL
        if not request.path.startswith(admin_url):
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))


class CitixenProfileMiddleware(MiddlewareMixin):
    """ Middleware for set profile """
    def process_request(self, request):
        admin_url = '/%s' % settings.ADMIN_URL
        if not request.path.startswith(admin_url):
            configs = getattr(settings, 'CITIXEN', {})
            self.__check_keys(configs)
            profile_finder = self.__import_finder(configs.get('PROFILE_FINDER', ''))
            profile = profile_finder(
                request.user,
                request.META.get(configs['APPLICATION_IDENTIFIER'], None),
                request.META.get(configs['HEADQUARTER_IDENTIFIER'], None),
            ).get()
            if not profile:
                raise PermissionDenied
            request.user.profile = profile

    @staticmethod
    def __check_keys(configs):
        if not {'HEADQUARTER_IDENTIFIER', 'APPLICATION_IDENTIFIER', 'PROFILE_FINDER'} <= set(configs):
            raise ImproperlyConfigured('Some keywords for profile middleware were not provided')

    @staticmethod
    def __import_finder(uri):
        try:
            path, class_name = uri.rsplit('.', 1)
            module = import_module(path)
            return getattr(module, class_name)
        except Exception:
            raise ImproperlyConfigured('Profile finder for middleware not configured correctly')
