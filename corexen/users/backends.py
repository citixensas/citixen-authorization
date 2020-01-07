from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from corexen.users.models import UserPermission


class AuthenticationBackend(ModelBackend):
    """Authentication backend.

    Customize user permissions checking.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_citixen_perm_cache'
        if not hasattr(user_obj, perm_cache_name):
            perms = UserPermission.objects.all()
            if not user_obj.is_superuser:
                perms = perms.filter(user=user_obj)
            perms = perms.filter(headquarter__isnull=False).values_list(
                'permission__content_type__app_label',
                'permission__codename',
                'headquarter'
            ).order_by()
            hq_perm_set = {"%s.%s.%s" % (ct, name, hq) for ct, name, hq in perms}
            setattr(user_obj, perm_cache_name, hq_perm_set)
        return getattr(user_obj, perm_cache_name)

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_citixen_perm_cache'):
            user_obj._citixen_perm_cache = {
                *self.get_user_permissions(user_obj),
            }
        return user_obj._citixen_perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        user_permissions = self.get_all_permissions(user_obj, obj)
        perm_in_all_permissions = perm in user_permissions
        return user_obj.is_active and perm_in_all_permissions
