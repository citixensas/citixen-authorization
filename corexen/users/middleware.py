from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from corexen.utils.customexception import process_exception, PermissionDenied


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
            # store the first part from the tuple (user, ob j)
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

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        admin_url = '/%s' % settings.ADMIN_URL
        exclude_custom_url = getattr(settings, 'EXCLUDE_URLS_PROFILE_FINDER', [])
        if not request.path.startswith(admin_url) and request.path not in exclude_custom_url:
            try:
                user = request.user
                if user.is_authenticated:
                    configs = getattr(settings, 'CITIXEN', {})
                    self.__check_keys(configs)
                    exclude_headquarter_validation = getattr(view_func.cls, 'exclude_headquarter_validation', False)
                    profile_finder = self.__import_finder(configs.get('PROFILE_FINDER', ''))
                    profile = profile_finder(
                        user=user,
                        app_id=request.META.get(configs['APPLICATION_IDENTIFIER'], None),
                        headquarter_id=request.META.get(configs['HEADQUARTER_IDENTIFIER'], None),
                        exclude_headquarter_validation=exclude_headquarter_validation
                    ).get()
                    if not profile:
                        raise PermissionDenied(_("Authenticated user without a valid profile"))
                    setattr(request, 'profile', profile)
                else:
                    setattr(request, 'profile', None)
            except ImproperlyConfigured as exc:
                raise ImproperlyConfigured(exc)
            except Exception as exc:
                return process_exception(exception=exc)

    @staticmethod
    def __check_keys(configs):
        if not {'HEADQUARTER_IDENTIFIER', 'APPLICATION_IDENTIFIER', 'PROFILE_FINDER'} <= set(configs):
            raise ImproperlyConfigured(_('Some keywords for profile middleware were not provided'))

    @staticmethod
    def __import_finder(uri):
        try:
            path, class_name = uri.rsplit('.', 1)
            module = import_module(path)
            return getattr(module, class_name)
        except Exception:
            raise ImproperlyConfigured(_('Profile finder for middleware not configured correctly'))
