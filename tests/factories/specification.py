import factory

from openapi_builder.specification import (
    Callback,
    Components,
    Contact,
    Discriminator,
    Encoding,
    Example,
    ExternalDocumentation,
    Header,
    Info,
    License,
    Link,
    MediaType,
    OAuthFlow,
    OAuthFlows,
    OpenAPI,
    Operation,
    Parameter,
    PathItem,
    Paths,
    Reference,
    RequestBody,
    Response,
    Responses,
    Schema,
    SecurityRequirement,
    SecurityScheme,
    Server,
    ServerVariable,
    Tag,
    missing,
)


class OpenAPIFactory(factory.Factory):
    class Meta:
        model = OpenAPI

    info = factory.SubFactory("tests.factories.specification.InfoFactory")
    paths = factory.SubFactory("tests.factories.specification.PathsFactory")
    servers = []
    components = factory.SubFactory("tests.factories.specification.ComponentsFactory")
    security = None
    tags = None
    external_docs = None


class InfoFactory(factory.Factory):
    class Meta:
        model = Info

    title = "title"
    version = "1.0.0"
    description = "description"
    terms_of_service = "terms_of_service"
    contact = factory.SubFactory("tests.factories.specification.ContactFactory")
    license = factory.SubFactory("tests.factories.specification.LicenseFactory")


class ContactFactory(factory.Factory):
    class Meta:
        model = Contact

    name = "name"
    email = "email"
    url = factory.Faker("url")


class LicenseFactory(factory.Factory):
    class Meta:
        model = License

    name = "name"
    url = factory.Faker("url")


class ServerFactory(factory.Factory):
    class Meta:
        model = Server

    url = "/"
    description = "description"
    variables = None


class ServerVariableFactory(factory.Factory):
    class Meta:
        model = ServerVariable

    enum = None
    default = None
    description = None


class ComponentsFactory(factory.Factory):
    class Meta:
        model = Components

    schemas = None
    responses = None
    parameters = None
    examples = None
    request_bodies = None
    headers = None
    security_schemes = None
    links = None
    callbacks = None


class PathsFactory(factory.Factory):
    class Meta:
        model = Paths

    values = {}


class PathItemFactory(factory.Factory):
    class Meta:
        model = PathItem

    ref = None
    summary = None
    description = None
    get = None
    put = None
    post = None
    delete = None
    options = None
    head = None
    patch = None
    trace = None
    servers = None
    parameters = None


class OperationFactory(factory.Factory):
    class Meta:
        model = Operation

    tags = None
    summary = None
    description = None
    external_docs = None
    operation_id = None
    parameters = None
    request_body = None
    responses = None
    callbacks = None
    deprecated = None
    security = None
    servers = None


class ExternalDocumentationFactory(factory.Factory):
    class Meta:
        model = ExternalDocumentation

    url = factory.Faker("url")
    description = "description"


class ParameterFactory(factory.Factory):
    class Meta:
        model = Parameter

    in_ = "query"
    name = "name"
    description = None
    schema = None
    required = True
    deprecated = False
    allow_empty_value = False


class RequestBodyFactory(factory.Factory):
    class Meta:
        model = RequestBody

    description = None
    content = {}
    required = False


class MediaTypeFactory(factory.Factory):
    class Meta:
        model = MediaType

    schema = None
    example = None
    examples = None
    encoding = None


class EncodingFactory(factory.Factory):
    class Meta:
        model = Encoding

    content_type = None
    headers = None
    style = None
    explode = True
    allow_reserved = False


class ResponsesFactory(factory.Factory):
    class Meta:
        model = Responses

    values = {}


class ResponseFactory(factory.Factory):
    class Meta:
        model = Response

    description = "description"
    headers = None
    content = None
    links = None


class CallbackFactory(factory.Factory):
    class Meta:
        model = Callback

    values = {}


class ExampleFactory(factory.Factory):
    class Meta:
        model = Example

    summary = None
    description = None
    value = None
    external_value = None


class LinkFactory(factory.Factory):
    class Meta:
        model = Link

    operation_ref = None
    operation_id = None
    parameters = None
    request_body = None
    description = None
    server = None


class HeaderFactory(factory.Factory):
    class Meta:
        model = Header

    description = None
    required = True
    deprecated = False
    allow_empty_value = False


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = "tag"
    description = None
    external_docs = None


class ReferenceFactory(factory.Factory):
    class Meta:
        model = Reference

    ref = "ref"
    required = True


class SchemaFactory(factory.Factory):
    class Meta:
        model = Schema

    title = None
    multiple_of = None
    maximum = None
    exclusive_maximum = None
    minimum = None
    exclusive_minimum = None
    max_length = None
    min_length = None
    pattern = None
    max_items = None
    min_items = None
    unique_items = None
    max_properties = None
    min_properties = None
    required = None
    enum = None
    type = None
    all_of = None
    any_of = None
    one_of = None
    not_ = None
    items = None
    properties = None
    additional_properties = True
    description = None
    format = None
    default = missing
    example = None
    examples = None


class DiscriminatorFactory(factory.Factory):
    class Meta:
        model = Discriminator

    property_name = "property_name"
    mapping = None


class SecuritySchemeFactory(factory.Factory):
    class Meta:
        model = SecurityScheme

    type = "http"
    name = "name"
    in_ = "query"
    scheme = "scheme"
    open_id_connect_url = factory.Faker("url")
    description = None
    bearer_format = None
    flows = []


class OAuthFlowsFactory(factory.Factory):
    class Meta:
        model = OAuthFlows

    implicit = None
    password = None
    client_credentials = None
    authorization_code = None


class OAuthFlowFactory(factory.Factory):
    class Meta:
        model = OAuthFlow

    authorization_url = factory.Faker("url")
    token_url = factory.Faker("url")
    refresh_url = None
    scopes = {}


class SecurityRequirementFactory(factory.Factory):
    class Meta:
        model = SecurityRequirement

    values = {}
