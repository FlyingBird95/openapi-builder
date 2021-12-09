import typing

from openapi_builder.specification import Schema

if typing.TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder


class Converter:
    """Converter for a certain class that returns a openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def __init__(self, builder: "OpenAPIBuilder", converts_class=None):
        self.builder: OpenAPIBuilder = builder
        self.builder.register_converter(self)
        if converts_class is not None:
            self.converts_class = converts_class

    def convert(self, value) -> Schema:
        raise NotImplementedError
