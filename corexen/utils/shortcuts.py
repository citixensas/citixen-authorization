from enum import Enum, EnumMeta


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
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
