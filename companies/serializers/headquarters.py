from rest_framework import serializers

from companies.models import Headquarter


class HeadquarterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headquarter
        fields = ('company', 'name', 'address', 'neighborhood', 'country', 'city', 'email', 'phone', 'is_active',)
        read_only_fields = ('is_active',)

    def create(self, validated_data):
        created_by = self.context['request'].user
        return Headquarter.objects.create(**validated_data, created_by=created_by)


class HeadquartersListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headquarter
        fields = ('pk', 'name', 'is_active',)
        read_only_fields = ('is_active',)
