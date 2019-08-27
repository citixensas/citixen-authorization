from factory.django import DjangoModelFactory
from faker import Factory

from corexen.permissions.models import GroupTemplate

fake = Factory.create()


class GroupTemplateFactory(DjangoModelFactory):
    class Meta:
        model = GroupTemplate


