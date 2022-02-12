import typing
import warnings


from openapi_builder.exceptions import MissingParameterConverter
from openapi_builder.specification import Schema

from .base import ParameterConverter
from .flask_converters import ALL_PARAMETER_CONVERTER_CLASSES

if typing.TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder


class ParameterManager:
    def __init__(self, builder: "OpenAPIBuilder"):
        self.builder: OpenAPIBuilder = builder
        self.converters: typing.List[ParameterConverter] = []

    def load_converters(self):
        """Load all converters, including the defaults."""
        for converter_class in self.options.parameter_converter_classes:
            self.register(converter_class)

        for converter_class in ALL_PARAMETER_CONVERTER_CLASSES:
            self.register(converter_class)

    def register(self, converter_class: typing.Type[ParameterConverter]):
        converter = converter_class(manager=self)
        self.converters.append(converter)

    def process(self, value: typing.Any):
        """Processes an instance, and returns a schema, or reference to that schema."""
        try:
            return next(
                converter.schema
                for converter in self.converters
                if converter.matches(value)
            )
        except StopIteration:
            if self.options.strict_mode == self.options.StrictMode.FAIL_ON_ERROR:
                raise MissingParameterConverter()
            elif self.options.strict_mode == self.options.StrictMode.SHOW_WARNINGS:
                warnings.warn(f"Missing converter for: {value}", UserWarning)
                return Schema(example="<unknown>")
            else:
                raise ValueError(f"Unknown strict mode: {self.options.strict_mode}")

    @property
    def options(self):
        return self.builder.options
