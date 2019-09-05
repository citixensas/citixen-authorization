from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class UserHeadquarterPermissions(DjangoModelPermissions):
    """"Allow user access to headquarters."""

    authenticated_users_only = True

    def __init__(self):
        """"""
        self.headquarter = None

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s.%(headquarter)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s.%(headquarter)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s.%(headquarter)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s.%(headquarter)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s.%(headquarter)s'],
    }

    def get_required_permissions(self, method, model_cls):
        headquarter = self.headquarter.pk if getattr(self, 'headquarter', None) else '-'
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name,
            'headquarter': headquarter
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        app_user = getattr(request.user, 'app_user', None)
        profile = getattr(app_user, 'profile', None) if app_user else None

        # Users without headquarter will be restricted with another logic.
        if profile and not profile.has_headquarter() or request.user.is_superuser:
            return True

        # Apply django model permissions
        self.headquarter = getattr(profile, 'headquarter', None)
        return super(UserHeadquarterPermissions, self).has_permission(request, view)


class IsSuperUserPermission(DjangoModelPermissions):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsCompanyManagerPermission(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        if request.user.has_company():
            return request.user.profile.company == obj
        return False
