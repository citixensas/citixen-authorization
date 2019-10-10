from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class UserHeadquarterPermissions(DjangoModelPermissions):
    """"Allow user access to headquarters."""

    authenticated_users_only = True

    def __init__(self):
        """"""
        self.headquarter = None
        self.custom_action = ''

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
        headquarter = self.headquarter.pk if self.headquarter else '-'
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name,
            'action_name': self.custom_action,
            'headquarter': headquarter
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)

        # Superusers can perform any action
        if request.user.is_superuser:
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
