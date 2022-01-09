from pytest_factoryboy import register

from tests.factories.builder import (
    DocumentationOptionsFactory,
    OpenApiDocumentationFactory,
)

register(DocumentationOptionsFactory)
register(OpenApiDocumentationFactory)
