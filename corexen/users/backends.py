from django.contrib.auth.backends import ModelBackend

from corexen.users.models import UserPermission


class AuthenticationBackend(ModelBackend):
    """Authentication backend.

    Customize user permissions checking.
    """

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
