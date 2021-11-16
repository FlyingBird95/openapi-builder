from openapi_generator.builder import SwaggerBuilder
from openapi_generator.specification import Schema


class Processor:
    """Processor for a certain class that returns a schema."""

    processes_class = None
    """Specification of the class that it processes."""

    @staticmethod
    def process(value, builder: "SwaggerBuilder") -> Schema:
        raise NotImplementedError
