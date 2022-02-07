import enum
import typing

from .base import DefaultsConverter

ALL_DEFAULT_CONVERTER_CLASSES = []


def append_converter_class(converter_class):
    ALL_DEFAULT_CONVERTER_CLASSES.append(converter_class)
    return converter_class


@append_converter_class
class VanillaConverter(DefaultsConverter):
    converts_class = (int, str, float)

    def convert(self, value) -> typing.Any:
        return value


@append_converter_class
class ListConverter(DefaultsConverter):
    converts_class = list

    def convert(self, value) -> typing.Any:
        return [self.manager.process(item) for item in value]


@append_converter_class
class CallableConverter(DefaultsConverter):
    def matches(self, value) -> bool:
        return callable(value)

    def convert(self, value) -> typing.Any:
        return self.manager.process(value())


@append_converter_class
class EnumConverter(DefaultsConverter):

    converts_class = enum.Enum

    def convert(self, value) -> typing.Any:
        return self.manager.process(value.value)


@append_converter_class
class NoneConverter(DefaultsConverter):
    def matches(self, value) -> bool:
        return value is None

    def convert(self, value) -> typing.Any:
        return None
