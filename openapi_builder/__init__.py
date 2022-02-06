from . import __meta__
from .builder import DocumentationOptions, OpenApiDocumentation
from .decorators import add_documentation, set_schema_options, set_resource_options

__version__ = __meta__.version

__all__ = [
    "DocumentationOptions",
    "OpenApiDocumentation",
    "add_documentation",
    "set_schema_options",
    "set_resource_options",
]
