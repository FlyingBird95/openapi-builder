import typing
import warnings

from openapi_builder.exceptions import MissingDefaultConverter

from .default_converters import ALL_DEFAULT_CONVERTER_CLASSES
from .base import DefaultsConverter

if typing.TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder


class DefaultsManager:
    def __init__(self, builder: "OpenAPIBuilder"):
        self.builder: OpenAPIBuilder = builder
        self.converters: typing.List[DefaultsConverter] = []

    def load_converters(self):
        """Load all converters, including the defaults."""
        for converter_class in self.options.defaults_converter_classes:
            self.register(converter_class)

        for converter_class in ALL_DEFAULT_CONVERTER_CLASSES:
            self.register(converter_class)

    def register(self, converter_class: typing.Type["DefaultsConverter"]):
        converter = converter_class(manager=self)
        self.converters.append(converter)

    def process(self, value: typing.Any):
        """Processes an instance, and returns a schema, or reference to that schema."""
        try:
            converter = next(
                converter for converter in self.converters if converter.matches(value)
            )
        except StopIteration:
            if self.options.strict_mode == self.options.StrictMode.FAIL_ON_ERROR:
                raise MissingDefaultConverter()
            elif self.options.strict_mode == self.options.StrictMode.SHOW_WARNINGS:
                warnings.warn(f"Missing converter for: {value}", UserWarning)
                return None
            else:
                raise ValueError(f"Unknown strict mode: {self.options.strict_mode}")
        else:
            return converter.convert(value=value)

    @property
    def options(self):
        return self.builder.options
