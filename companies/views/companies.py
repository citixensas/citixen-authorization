"""Company view"""

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from companies.serializers import (CompanyModelSerializer,
                                           CompanyListModelSerializer,
                                           HeadquartersListModelSerializer)
from companies.models import Company, Headquarter
from companies.permissions import IsCompanyManagerPermission


class CompanyViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer

    def list(self, request, *args, **kwargs):
        companies = Company.objects.all()
        serializer = self.get_serializer(companies, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """Modifica los permisos en base a la acción que desee realizar"""
        permissions = [IsAuthenticated]
        if self.action in ['retrieve', 'headquarters'] and not self.request.user.is_superuser:
            permissions.append(IsCompanyManagerPermission)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Retorna el serializador basado en la acción a realizar"""
        if self.action == 'list':
            return CompanyListModelSerializer
        return super(CompanyViewSet, self).get_serializer_class()

    @action(methods=['GET'], detail=True)
    def headquarters(self, request, pk=None):
        queryset = Headquarter.objects.all()
        headquarters = queryset.filter(company=pk)
        serializer = HeadquartersListModelSerializer(headquarters, many=True)
        return Response(serializer.data)
