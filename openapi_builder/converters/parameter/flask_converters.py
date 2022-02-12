"""Contains all parameter converters for flask.current_app.url_map._converters."""
from werkzeug.routing import (
    AnyConverter,
    FloatConverter,
    IntegerConverter,
    PathConverter,
    UnicodeConverter,
    UUIDConverter,
)

from openapi_builder.specification import Schema

from .base import ParameterConverter


ALL_PARAMETER_CONVERTER_CLASSES = []


def append_converter_class(converter_class):
    ALL_PARAMETER_CONVERTER_CLASSES.append(converter_class)
    return converter_class


@append_converter_class
class UnicodeParameterConverter(ParameterConverter):
    converts_class = UnicodeConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@append_converter_class
class AnyParameterConverter(ParameterConverter):
    converts_class = AnyConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@append_converter_class
class PathParameterConverter(ParameterConverter):
    converts_class = PathConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@append_converter_class
class IntParameterConverter(ParameterConverter):
    converts_class = IntegerConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="number", format="integer")


@append_converter_class
class FloatParameterConverter(ParameterConverter):
    converts_class = FloatConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="number", format="float")


@append_converter_class
class UUIDParameterConverter(ParameterConverter):
    converts_class = UUIDConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="hex")
