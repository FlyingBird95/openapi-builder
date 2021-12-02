from . import __meta__
from .builder import DocumentationOptions, OpenApiDocumentation
from .decorators import add_documentation

__version__ = __meta__.version

__all__ = [
    "add_documentation",
    "DocumentationOptions",
    "OpenApiDocumentation",
]
