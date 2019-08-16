"""Citixen serializer utilities."""

from abc import ABC

from rest_framework import serializers
from rest_framework.relations import PKOnlyObject


class CitixenRelatedField(serializers.RelatedField, ABC):
    """Base Citixen related field."""

    serializer_class = None

    def to_representation(self, value):
        """Conver model value to serialized data."""
        if type(value) == PKOnlyObject:
            value = self.queryset.get(pk=value.pk)
        return self.serializer_class(value).data if value else None


class CitixenPrimaryKeyRelatedField(CitixenRelatedField,
                                    serializers.PrimaryKeyRelatedField):
    """Citixen primary key related field."""

    def __init__(self, **kwargs):
        self.serializer_class = kwargs.pop('serializer_class', None)
        assert self.serializer_class is not None, '`serializer_class` is a required argument.'
        super().__init__(**kwargs)



class CitixenModelSerializer(serializers.ModelSerializer):
    """Custom citixen model serializer."""

    perms_map = {
        'GET': 'view_%(model_name)s',
        'POST': 'add_%(model_name)s',
        'PUT': 'change_%(model_name)s',
        'PATCH': 'change_%(model_name)s',
        'DELETE': 'delete_%(model_name)s',
    }

    def has_permission_in_company(self):
        raise NotImplementedError

    def has_permission_in_headquarter(self):
        if self.headquarter:
            method = self.context['request'].method.upper()
            model_name = self.Meta.model._meta.model_name
            perm = self.perms_map[method] % {'model_name': model_name}
            return self.context['request'].user.permissions.filter(
                permission__codename=perm, headquarter=getattr(self, 'headquarter', None)
            ).exist()
        return False

    def validate(self, attrs):
        self.has_permission_in_headquarter()
        self.has_permission_in_company()
        return super(CitixenModelSerializer, self).validate(attrs)
