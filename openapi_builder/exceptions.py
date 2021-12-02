from openapi_builder.util import to_camelcase

MISSING_PROCESSOR_MESSAGE = '''
You're missing a processor for class {class_name}.
You can use the snippet below to generate a processor for it. Don't forget to register it!


from typing import Union

from openapi_builder.builder import OpenAPIBuilder
from openapi_builder.processors import Processor
from openapi_builder.specification import Reference, Schema

class {class_name}Processor(Processor):
    """Processor for a certain class that returns a schema."""

    processes_class = {class_name}
    """Specification of the class that it processes."""

    @staticmethod
    def process(value: {class_name}, builder: OpenAPIBuilder) -> Union[Reference, Schema]:
        """Processes an instance of {class_name} and return a Reference or Schema."""
'''


class OpenApiException(Exception):
    """Base Exception."""


class MissingProcessor(OpenApiException):
    """Missing processor for the given class."""

    def __init__(self, value):
        class_name = value.__class__.__name__
        super().__init__(
            MISSING_PROCESSOR_MESSAGE.format(class_name=to_camelcase(class_name))
        )
