from openapi_builder.exceptions import MissingParameterConverter
from openapi_builder.specification import Parameter

from .base import PARAMETER_CONVERTERS


def process_parameter(converter_class):
    try:
        converter = next(
            converter
            for converter in PARAMETER_CONVERTERS
            if converter.matches(converter_class)
        )
    except StopIteration:
        raise MissingParameterConverter()

    return converter.schema


def parse_openapi_arguments(rule):
    """Parsers parameter objects."""
    parameters = []

    for argument, converter_class in rule._converters.items():
        schema = process_parameter(converter_class)
        parameters.append(
            Parameter(name=argument, in_="path", required=True, schema=schema)
        )

    return parameters
