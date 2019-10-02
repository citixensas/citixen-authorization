"""Groups admin"""

from django.contrib import admin

from corexen.permissions.models import GroupTemplate, GroupTemplatePermission


class PermissionInline(admin.AllValuesFieldListFilter):
    model = GroupTemplatePermission
    extra = 3


@admin.register(GroupTemplate)
class GroupAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'parent', 'headquarter')
    list_filter = ('parent', 'headquarter')


