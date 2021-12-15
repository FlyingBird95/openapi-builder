import factory
from pytest_factoryboy import LazyFixture

from openapi_builder import DocumentationOptions, OpenApiDocumentation


class DocumentationOptionsFactory(factory.Factory):
    class Meta:
        model = DocumentationOptions

    include_head_response = True
    include_options_response = True
    server_url = "/"
    include_marshmallow_converters = True
    include_documentation_blueprint = True


class OpenApiDocumentationFactory(factory.Factory):
    class Meta:
        model = OpenApiDocumentation

    app = LazyFixture("app")
    options = factory.SubFactory(DocumentationOptionsFactory)
