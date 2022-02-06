import typing

from openapi_builder.specification import Schema

if typing.TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder

CONVERTER_CLASSES: typing.List[typing.Type["Converter"]] = []


def register_converter(converter_class):
    """Decorator for registering a converter.

    The Converter is instantiated on initialization of the OpenApiBuilder.
    """
    CONVERTER_CLASSES.append(converter_class)
    return converter_class


class Converter:
    """Converter for a certain class that returns a openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def __init__(self, builder: "OpenAPIBuilder"):
        self.builder: OpenAPIBuilder = builder

    def matches(self, value) -> bool:
        """Returns True if the Converter can match the specified class."""
        return isinstance(value, self.converts_class)

    def convert(self, value, name) -> Schema:
        raise NotImplementedError
