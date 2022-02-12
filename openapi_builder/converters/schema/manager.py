import typing
import warnings

from openapi_builder.exceptions import MissingConverter
from openapi_builder.specification import Schema

from .base import SchemaConverter

if typing.TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder


class SchemaManager:
    exception_class = MissingConverter

    def __init__(self, builder: "OpenAPIBuilder"):
        self.builder: OpenAPIBuilder = builder
        self.converters: typing.List[SchemaConverter] = []

    def load_converters(self):
        """Load all converters, including the defaults."""
        for converter_class in self.options.schema_converter_classes:
            self.register(converter_class)

        if self.options.include_marshmallow_converters:
            # Import locally, because not everyone uses marshmallow
            from .marshmallow import ALL_MARSHMALLOW_CONVERTER_CLASSES

            for converter_class in ALL_MARSHMALLOW_CONVERTER_CLASSES:
                self.register(converter_class)

        if self.options.include_halogen_converters:
            # Import locally, because not everyone uses halogen
            from .halogen import ALL_HALOGEN_CONVERTER_CLASSES

            for converter_class in ALL_HALOGEN_CONVERTER_CLASSES:
                self.register(converter_class)

    def register(self, converter_class: typing.Type[SchemaConverter]):
        converter = converter_class(manager=self)
        self.converters.append(converter)

    def process(self, value: typing.Any, name: str):
        """Processes an instance, and returns a schema, or reference to that schema."""
        try:
            converter = next(
                converter for converter in self.converters if converter.matches(value)
            )
        except StopIteration:
            if self.options.strict_mode == self.options.StrictMode.FAIL_ON_ERROR:
                raise self.exception_class()
            elif self.options.strict_mode == self.options.StrictMode.SHOW_WARNINGS:
                warnings.warn(f"Missing converter for: {value}: {name}", UserWarning)
                return Schema(example="<unknown>")
            else:
                raise ValueError(f"Unknown strict mode: {self.options.strict_mode}")
        else:
            return converter.convert(value=value, name=name)

    @property
    def options(self):
        return self.builder.options
