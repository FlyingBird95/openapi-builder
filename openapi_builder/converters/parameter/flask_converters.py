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

from .base import ParameterConverter, register_parameter_converter


@register_parameter_converter
class UnicodeParameterConverter(ParameterConverter):
    converts_class = UnicodeConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@register_parameter_converter
class AnyParameterConverter(ParameterConverter):
    converts_class = AnyConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@register_parameter_converter
class PathParameterConverter(ParameterConverter):
    converts_class = PathConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="string")


@register_parameter_converter
class IntParameterConverter(ParameterConverter):
    converts_class = IntegerConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="number", format="integer")


@register_parameter_converter
class FloatParameterConverter(ParameterConverter):
    converts_class = FloatConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="number", format="float")


@register_parameter_converter
class UUIDParameterConverter(ParameterConverter):
    converts_class = UUIDConverter

    @property
    def schema(self) -> Schema:
        return Schema(type="string", format="hex")
