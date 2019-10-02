# Rest-Framework
from django.contrib.auth.models import Permission
from rest_framework import serializers

# Citixen
from corexen.permissions.models.group import GroupTemplate, GroupTemplatePermission


class GroupTemplateModelSerializer(serializers.ModelSerializer):

    groups = serializers.SerializerMethodField()

    class Meta:
        model = GroupTemplate
        fields = [
            'pk',
            'name',
            'parent',
            'group_permissions',
            'headquarter',
            'groups'
        ]
        read_only_fields = ['pk']

    def validate(self, attrs):
        if self.initial_data.get('group_permissions', None):
            permissions = self.initial_data["group_permissions"]
            permissions_instances = Permission.objects.filter(pk__in=permissions)
            if permissions_instances.count() == len(permissions):
                self.context['permissions_instances'] = permissions_instances
            else:
                raise serializers.ValidationError({'group_permissions': "permission parameter does not exist"})
        return attrs

    def create(self, validated_data):
        group = GroupTemplate.objects.create(**validated_data)
        group_perms = []
        if self.context.get('permissions_instances', None):
            for permission in self.context['permissions_instances']:
                group_perms.append(GroupTemplatePermission(group=group, permission=permission))
            GroupTemplatePermission.objects.bulk_create(group_perms)
        group.save()
        return group

    def update(self, instance, validated_data):
        GroupTemplatePermission.objects.filter(group=instance).delete()
        group_perms = []
        if self.context['permissions_instances']:
            for permission in self.context['permissions_instances']:
                group_perms.append(GroupTemplatePermission(group=instance, permission=permission))
            GroupTemplatePermission.objects.bulk_create(group_perms)
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

    def get_groups(self, obj):
        children = obj.get_children()
        return GroupTemplateModelSerializer(children, many=True).data

