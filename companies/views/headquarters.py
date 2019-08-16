"""Headquarters view"""

from rest_framework import viewsets

from companies.serializers import HeadquarterModelSerializer, HeadquartersListModelSerializer
from companies.models import Headquarter


class HeadquartersViewSet(viewsets.ModelViewSet):
    queryset = Headquarter.objects.all()

    def perform_destroy(self, instance):
        instance.mark_as_delete()

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_superuser:
            profile = self.request.user.profile
            has_company = self.request.user.has_company()
            company = profile.company if has_company else profile.headquarter.company
            queryset = queryset.filter(company=company, is_deleted=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return HeadquartersListModelSerializer
        return HeadquarterModelSerializer
