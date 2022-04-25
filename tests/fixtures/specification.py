from pytest_factoryboy import register

from tests.factories.specification import (
    CallbackFactory,
    ComponentsFactory,
    ContactFactory,
    DiscriminatorFactory,
    EncodingFactory,
    ExampleFactory,
    ExternalDocumentationFactory,
    HeaderFactory,
    InfoFactory,
    LicenseFactory,
    LinkFactory,
    MediaTypeFactory,
    OAuthFlowFactory,
    OAuthFlowsFactory,
    OpenAPIFactory,
    OperationFactory,
    ParameterFactory,
    PathItemFactory,
    PathsFactory,
    ReferenceFactory,
    RequestBodyFactory,
    ResponseFactory,
    ResponsesFactory,
    SchemaFactory,
    SecurityRequirementFactory,
    SecuritySchemeFactory,
    ServerFactory,
    ServerVariableFactory,
    TagFactory,
)

register(OpenAPIFactory)
register(InfoFactory)
register(ContactFactory)
register(LicenseFactory)
register(ServerFactory)
register(ServerVariableFactory)
register(ComponentsFactory)
register(PathsFactory)
register(PathItemFactory)
register(OperationFactory)
register(ExternalDocumentationFactory)
register(ParameterFactory)
register(RequestBodyFactory)
register(MediaTypeFactory)
register(EncodingFactory)
register(ResponsesFactory)
register(ResponseFactory)
register(CallbackFactory)
register(ExampleFactory)
register(LinkFactory)
register(HeaderFactory)
register(TagFactory)
register(ReferenceFactory)
register(SchemaFactory)
register(SchemaFactory, "second_schema")
register(DiscriminatorFactory)
register(SecuritySchemeFactory)
register(OAuthFlowsFactory, "oauth_flows")
register(OAuthFlowFactory, "oauth_flow")
register(OAuthFlowFactory, "second_oauth_flow")
register(SecurityRequirementFactory)
