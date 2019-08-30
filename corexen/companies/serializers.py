from rest_framework import serializers

from corexen.companies.models import Company, Headquarter


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('nit', 'name', 'email', 'country', 'is_active',)
        read_only_fields = ('is_active',)


class CompanyListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('pk', 'name',)


class HeadquarterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headquarter
        fields = ('company', 'name', 'address', 'neighborhood', 'country', 'city', 'email', 'phone', 'is_active',)
        read_only_fields = ('is_active',)

    def create(self, validated_data):
        created_by = self.context['request'].user.uuid  # Only for superusers
        return Headquarter.objects.create(**validated_data, created_by=created_by)


class HeadquartersListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headquarter
        fields = ('pk', 'name', 'is_active',)
        read_only_fields = ('is_active',)
