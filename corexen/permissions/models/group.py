"""Groups model"""
from corexen.companies.models import Headquarter
from django.db import models

from corexen.utils.models import CitixenModel


class GroupTemplate(CitixenModel):

    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    group_permissions = models.ManyToManyField('auth.Permission', through='permissions.GroupTemplatePermission',
                                               verbose_name='group_permissions', blank=True,)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.DO_NOTHING)

    def get_children(self):
        return GroupTemplate.objects.filter(parent=self)

    def __str__(self):
        return f'{self.name}'

class GroupTemplatePermission(CitixenModel):
    group = models.ForeignKey('permissions.GroupTemplate', on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.DO_NOTHING)

