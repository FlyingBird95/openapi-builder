import typing
from abc import ABC

from openapi_builder.specification import Schema

if typing.TYPE_CHECKING:
    from .manager import SchemaManager


class SchemaConverter(ABC):
    """Converter for a certain class that returns an openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def __init__(self, manager: "SchemaManager"):
        self.manager: SchemaManager = manager

    def matches(self, value) -> bool:
        """Returns True if the Converter can match the specified class."""
        return isinstance(value, self.converts_class)

    def convert(self, value, name) -> Schema:
        raise NotImplementedError()
