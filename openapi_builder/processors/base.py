import typing

from openapi_builder.specification import Schema

if typing.TYPE_CHECKING:
    from openapi_builder import OpenAPIBuilder


class Processor:
    """Processor for a certain class that returns a schema."""

    processes_class = None
    """Specification of the class that it processes."""

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        raise NotImplementedError
