from openapi_builder.util import to_camelcase

MISSING_PROCESSOR_MESSAGE = '''
You're missing a converter for class {class_name}.
You can use the snippet below to generate a converter for it. Don't forget to register it!


from typing import Union

from openapi_builder.builder import OpenAPIBuilder
from openapi_builder.converts import Converter
from openapi_builder.specification import Reference, Schema

class {class_name}Converter(Converter):
    """Converter for a certain class that returns a openapi_builder.specification.Schema."""

    converts_class = {class_name}
    """Specification of the class that it converts."""

    def convert(value: {class_name}) -> Union[Reference, Schema]:
        """Converts an instance of {class_name} and return a Reference or Schema."""
'''

MISSING_CONFIG_CONTEXT = """
You're not allowed to call this function outside the use_documentation_config context manager.
Please call the function in the following manner:

>>> builder = OpenAPIBuilder()
>>> config = Documentation()  # retrieved from the @add_documentation decorator.
>>> with builder.use_documentation_config():
>>>     builder.your_function()
"""


class OpenApiException(Exception):
    """Base Exception."""


class MissingConverter(OpenApiException):
    """Missing converter for the given class or instance."""

    def __init__(self, value):
        class_name = value.__class__.__name__
        super().__init__(
            MISSING_PROCESSOR_MESSAGE.format(class_name=to_camelcase(class_name))
        )


class MissingConfigContext(OpenApiException):
    """Missing config context.

    The function must be called inside the 'use_documentation_config' context manager.
    """

    def __init__(self):
        super().__init__(MISSING_CONFIG_CONTEXT)
