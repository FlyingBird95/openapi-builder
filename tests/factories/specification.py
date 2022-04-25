from dataclasses import Field, MISSING, is_dataclass

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
)


def inspect_default(class_to_inspect, variable):
    if not is_dataclass(class_to_inspect):
        raise Exception(
            "This function is only allowed for classes decorated with @dataclass"
        )
    try:
        field: Field = class_to_inspect.__dataclass_fields__[variable]
    except KeyError:
        raise Exception(f"Unknown property {class_to_inspect}.{variable}")
    if field.default is not MISSING:
        return field.default
    if field.default_factory is not MISSING:
        return field.default_factory()

    raise Exception(f"Unknown default for '{class_to_inspect}'.{variable}")


class OpenAPIFactory(factory.Factory):
    class Meta:
        model = OpenAPI

    info = factory.SubFactory("tests.factories.specification.InfoFactory")
    paths = inspect_default(OpenAPI, "paths")
    servers = inspect_default(OpenAPI, "servers")
    components = inspect_default(OpenAPI, "components")
    security = inspect_default(OpenAPI, "security")
    tags = inspect_default(OpenAPI, "tags")
    external_docs = inspect_default(OpenAPI, "external_docs")


class InfoFactory(factory.Factory):
    class Meta:
        model = Info

    title = "title"
    version = "1.0.0"
    description = inspect_default(Info, "description")
    terms_of_service = inspect_default(Info, "terms_of_service")
    contact = inspect_default(Info, "contact")
    license = inspect_default(Info, "license")


class ContactFactory(factory.Factory):
    class Meta:
        model = Contact

    name = inspect_default(Contact, "name")
    email = inspect_default(Contact, "email")
    url = inspect_default(Contact, "url")


class LicenseFactory(factory.Factory):
    class Meta:
        model = License

    name = factory.Faker("name")
    url = inspect_default(License, "url")


class ServerFactory(factory.Factory):
    class Meta:
        model = Server

    url = factory.Faker("url")
    description = inspect_default(Server, "description")
    variables = inspect_default(Server, "variables")


class ServerVariableFactory(factory.Factory):
    class Meta:
        model = ServerVariable

    default = "default"
    enum = inspect_default(ServerVariable, "enum")
    description = inspect_default(ServerVariable, "description")


class ComponentsFactory(factory.Factory):
    class Meta:
        model = Components

    schemas = inspect_default(Components, "schemas")
    responses = inspect_default(Components, "responses")
    parameters = inspect_default(Components, "parameters")
    examples = inspect_default(Components, "examples")
    request_bodies = inspect_default(Components, "request_bodies")
    headers = inspect_default(Components, "headers")
    security_schemes = inspect_default(Components, "security_schemes")
    links = inspect_default(Components, "links")
    callbacks = inspect_default(Components, "callbacks")


class PathsFactory(factory.Factory):
    class Meta:
        model = Paths

    values = inspect_default(Paths, "values")


class PathItemFactory(factory.Factory):
    class Meta:
        model = PathItem

    ref = inspect_default(PathItem, "ref")
    summary = inspect_default(PathItem, "summary")
    description = inspect_default(PathItem, "description")
    get = inspect_default(PathItem, "get")
    put = inspect_default(PathItem, "put")
    post = inspect_default(PathItem, "post")
    delete = inspect_default(PathItem, "delete")
    options = inspect_default(PathItem, "options")
    head = inspect_default(PathItem, "head")
    patch = inspect_default(PathItem, "patch")
    trace = inspect_default(PathItem, "trace")
    servers = inspect_default(PathItem, "servers")
    parameters = inspect_default(PathItem, "parameters")


class OperationFactory(factory.Factory):
    class Meta:
        model = Operation

    tags = inspect_default(Operation, "tags")
    summary = inspect_default(Operation, "summary")
    description = inspect_default(Operation, "description")
    external_docs = inspect_default(Operation, "external_docs")
    operation_id = inspect_default(Operation, "operation_id")
    parameters = inspect_default(Operation, "parameters")
    request_body = inspect_default(Operation, "request_body")
    responses = inspect_default(Operation, "responses")
    callbacks = inspect_default(Operation, "callbacks")
    deprecated = inspect_default(Operation, "deprecated")
    security = inspect_default(Operation, "security")
    servers = inspect_default(Operation, "servers")


class ExternalDocumentationFactory(factory.Factory):
    class Meta:
        model = ExternalDocumentation

    url = factory.Faker("url")
    description = inspect_default(ExternalDocumentation, "description")


class ParameterFactory(factory.Factory):
    class Meta:
        model = Parameter

    in_ = "query"
    name = "name"
    description = inspect_default(Parameter, "description")
    schema = inspect_default(Parameter, "schema")
    required = inspect_default(Parameter, "required")
    deprecated = inspect_default(Parameter, "deprecated")
    allow_empty_value = inspect_default(Parameter, "allow_empty_value")


class RequestBodyFactory(factory.Factory):
    class Meta:
        model = RequestBody

    description = inspect_default(RequestBody, "description")
    content = inspect_default(RequestBody, "content")
    required = inspect_default(RequestBody, "required")


class MediaTypeFactory(factory.Factory):
    class Meta:
        model = MediaType

    schema = inspect_default(MediaType, "schema")
    example = inspect_default(MediaType, "example")
    examples = inspect_default(MediaType, "examples")
    encoding = inspect_default(MediaType, "encoding")


class EncodingFactory(factory.Factory):
    class Meta:
        model = Encoding

    content_type = inspect_default(Encoding, "content_type")
    headers = inspect_default(Encoding, "headers")
    style = inspect_default(Encoding, "style")
    explode = inspect_default(Encoding, "explode")
    allow_reserved = inspect_default(Encoding, "allow_reserved")


class ResponsesFactory(factory.Factory):
    class Meta:
        model = Responses

    values = inspect_default(Responses, "values")


class ResponseFactory(factory.Factory):
    class Meta:
        model = Response

    description = "description"
    headers = inspect_default(Response, "headers")
    content = inspect_default(Response, "content")
    links = inspect_default(Response, "links")


class CallbackFactory(factory.Factory):
    class Meta:
        model = Callback

    values = inspect_default(Callback, "values")


class ExampleFactory(factory.Factory):
    class Meta:
        model = Example

    summary = inspect_default(Example, "summary")
    description = inspect_default(Example, "description")
    value = inspect_default(Example, "value")
    external_value = inspect_default(Example, "external_value")


class LinkFactory(factory.Factory):
    class Meta:
        model = Link

    operation_ref = inspect_default(Link, "operation_ref")
    operation_id = inspect_default(Link, "operation_id")
    parameters = inspect_default(Link, "parameters")
    request_body = inspect_default(Link, "request_body")
    description = inspect_default(Link, "description")
    server = inspect_default(Link, "server")


class HeaderFactory(factory.Factory):
    class Meta:
        model = Header

    description = inspect_default(Header, "description")
    required = inspect_default(Header, "required")
    deprecated = inspect_default(Header, "deprecated")
    allow_empty_value = inspect_default(Header, "allow_empty_value")


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = "tag"
    description = inspect_default(Tag, "description")
    external_docs = inspect_default(Tag, "external_docs")


class ReferenceFactory(factory.Factory):
    class Meta:
        model = Reference

    ref = "ref"
    required = True


class SchemaFactory(factory.Factory):
    class Meta:
        model = Schema

    title = inspect_default(Schema, "title")
    multiple_of = inspect_default(Schema, "multiple_of")
    maximum = inspect_default(Schema, "maximum")
    exclusive_maximum = inspect_default(Schema, "exclusive_maximum")
    minimum = inspect_default(Schema, "minimum")
    exclusive_minimum = inspect_default(Schema, "exclusive_minimum")
    max_length = inspect_default(Schema, "max_length")
    min_length = inspect_default(Schema, "min_length")
    pattern = inspect_default(Schema, "pattern")
    max_items = inspect_default(Schema, "max_items")
    min_items = inspect_default(Schema, "min_items")
    unique_items = inspect_default(Schema, "unique_items")
    max_properties = inspect_default(Schema, "max_properties")
    min_properties = inspect_default(Schema, "min_properties")
    required = inspect_default(Schema, "required")
    enum = inspect_default(Schema, "enum")
    type = inspect_default(Schema, "type")
    all_of = inspect_default(Schema, "all_of")
    any_of = inspect_default(Schema, "any_of")
    one_of = inspect_default(Schema, "one_of")
    not_ = inspect_default(Schema, "not_")
    items = inspect_default(Schema, "items")
    properties = inspect_default(Schema, "properties")
    additional_properties = inspect_default(Schema, "additional_properties")
    description = inspect_default(Schema, "description")
    format = inspect_default(Schema, "format")
    default = inspect_default(Schema, "default")
    example = inspect_default(Schema, "example")
    examples = inspect_default(Schema, "examples")
    discriminator = inspect_default(Schema, "discriminator")


class DiscriminatorFactory(factory.Factory):
    class Meta:
        model = Discriminator

    property_name = "property_name"
    mapping = inspect_default(Discriminator, "mapping")


class SecuritySchemeFactory(factory.Factory):
    class Meta:
        model = SecurityScheme

    type = "http"
    in_ = "query"
    name = inspect_default(SecurityScheme, "name")
    scheme = inspect_default(SecurityScheme, "scheme")
    open_id_connect_url = inspect_default(SecurityScheme, "open_id_connect_url")
    description = inspect_default(SecurityScheme, "description")
    bearer_format = inspect_default(SecurityScheme, "bearer_format")
    flows = inspect_default(SecurityScheme, "flows")


class OAuthFlowsFactory(factory.Factory):
    class Meta:
        model = OAuthFlows

    implicit = inspect_default(OAuthFlows, "implicit")
    password = inspect_default(OAuthFlows, "password")
    client_credentials = inspect_default(OAuthFlows, "client_credentials")
    authorization_code = inspect_default(OAuthFlows, "authorization_code")


class OAuthFlowFactory(factory.Factory):
    class Meta:
        model = OAuthFlow

    authorization_url = factory.Faker("url")
    token_url = factory.Faker("url")
    refresh_url = inspect_default(OAuthFlow, "refresh_url")
    scopes = inspect_default(OAuthFlow, "scopes")


class SecurityRequirementFactory(factory.Factory):
    class Meta:
        model = SecurityRequirement

    values = inspect_default(SecurityRequirement, "values")
