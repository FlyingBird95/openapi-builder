import typing

from openapi_builder.specification import Schema

PARAMETER_CONVERTERS: typing.List["ParameterConverter"] = []


def register_parameter_converter(converter_class):
    """Decorator for registering a converter.

    The parameter converter is initialized without any arguments.
    """
    instance = converter_class()
    PARAMETER_CONVERTERS.append(instance)
    return converter_class


class ParameterConverter:
    """Converter for a certain class that returns an openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def matches(self, value) -> bool:
        """Returns True if the Converter can match the specified class."""
        return isinstance(value, self.converts_class)

    @property
    def schema(self) -> Schema:
        raise NotImplementedError
