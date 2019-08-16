from rest_framework.permissions import DjangoModelPermissions


class IsCompanyManagerPermission(DjangoModelPermissions):

    def has_object_permission(self, request, view, obj):
        if request.user.has_company():
            return request.user.profile.company == obj
        return False
