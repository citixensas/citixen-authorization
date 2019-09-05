from django.utils.deprecation import MiddlewareMixin

_ORG_TYPES = ['headquarter', 'company']


def _assign_company_and_headquarter_to_request(request):
    for org_type in _ORG_TYPES:
        if hasattr(request.user, 'profile'):
            setattr(request, org_type, getattr(request.user.profile, org_type, None))
        else:
            setattr(request, org_type, None)


class UserContextOrganizationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            _assign_company_and_headquarter_to_request(request)
