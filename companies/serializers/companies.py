from rest_framework import serializers

from companies.models import Company


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('nit', 'name', 'email', 'country', 'is_active',)
        read_only_fields = ('is_active',)


class CompanyListModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('pk', 'name',)
