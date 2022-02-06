import enum
import typing

from .base import DefaultConverter, register_default_converter
from .process import get_default


@register_default_converter
class VanillaConverter(DefaultConverter):
    converts_class = (int, str, float)

    def convert(self, value) -> typing.Any:
        return value


@register_default_converter
class ListConverter(DefaultConverter):
    converts_class = list

    def convert(self, value) -> typing.Any:
        return [get_default(item) for item in value]


@register_default_converter
class CallableConverter(DefaultConverter):
    def matches(self, value) -> bool:
        return callable(value)

    def convert(self, value) -> typing.Any:
        return get_default(value())


@register_default_converter
class EnumConverter(DefaultConverter):

    converts_class = enum.Enum

    def convert(self, value) -> typing.Any:
        return get_default(value.value)


@register_default_converter
class NoneConverter(DefaultConverter):
    def matches(self, value) -> bool:
        return value is None

    def convert(self, value) -> typing.Any:
        return None
