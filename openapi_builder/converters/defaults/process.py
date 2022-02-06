from openapi_builder.exceptions import MissingDefaultConverter

from .base import DEFAULT_CONVERTERS


def get_default(value):
    try:
        converter = next(
            converter for converter in DEFAULT_CONVERTERS if converter.matches(value)
        )
    except StopIteration:
        raise MissingDefaultConverter()

    return converter.convert(value)
