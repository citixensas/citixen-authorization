"""Group view"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from corexen.permissions.models import GroupTemplate
from corexen.permissions.serializers import GroupTemplateModelSerializer


class GroupTemplateViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           GenericViewSet):
    queryset = GroupTemplate.objects.all()
    serializer_class = GroupTemplateModelSerializer

    def get_queryset(self):
        queryset = super(GroupTemplateViewSet, self).get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(parent=None)
        return queryset

    def create(self, request, *args, **kwargs):
        group_template_serializer = GroupTemplateModelSerializer(
            data=request.data,
            context={
                'user': request.user
            }
        )
        group_template_serializer.is_valid(raise_exception=True)
        group_template_serializer.save()

        return Response(data=group_template_serializer.data, status=status.HTTP_201_CREATED)
