from enum import Enum, EnumMeta

from django.shortcuts import _get_queryset


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


class DirectValueMetaClass(EnumMeta):

    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value[0]
        return value


class CitixenChoices(Enum, metaclass=DirectValueMetaClass):
    @classmethod
    def choices(cls):
        return tuple((i.value[0], i.value[1]) for i in cls if (bool(i.value[2]) if 2 < len(i.value) else True))
