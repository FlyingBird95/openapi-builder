import typing

DEFAULT_CONVERTERS: typing.List["DefaultConverter"] = []


def register_default_converter(converter_class):
    """Decorator for registering a converter.

    The default converter is initialized without any arguments.
    """
    instance = converter_class()
    DEFAULT_CONVERTERS.append(instance)
    return converter_class


class DefaultConverter:
    """Converter for a certain class that returns a openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def matches(self, value) -> bool:
        """Returns True if the Converter can match the specified class."""
        return isinstance(value, self.converts_class)

    def convert(self, value) -> typing.Any:
        raise NotImplementedError
