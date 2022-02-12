import typing
from abc import ABC

if typing.TYPE_CHECKING:
    from .manager import DefaultsManager


class DefaultsConverter(ABC):
    """Converter for a certain class that returns an openapi_builder.specification.Schema."""

    converts_class = None
    """Specification of the class that it converts."""

    def __init__(self, manager: "DefaultsManager"):
        self.manager: DefaultsManager = manager

    def matches(self, value) -> bool:
        """Returns True if the Converter can match the specified class."""
        return isinstance(value, self.converts_class)

    def convert(self, value) -> typing.Any:
        raise NotImplementedError
