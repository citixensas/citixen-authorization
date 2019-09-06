from enum import Enum, EnumMeta


class DirectValueMetaClass(EnumMeta):

    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value[0]
        return value


class CitixenChoices(Enum, metaclass=DirectValueMetaClass):
    @classmethod
    def choices(cls):
        return tuple((i.value[0], i.value[1]) for i in cls)