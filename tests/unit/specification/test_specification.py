import pytest
from pytest_factoryboy import LazyFixture

from openapi_builder.specification import Reference, Response


def test_openapi(open_api, info):
    assert open_api.get_value() == {
        "openapi": "3.0.3",
        "info": info.get_value(),
        "servers": [],
        "paths": {},
        "components": {},
    }


@pytest.mark.parametrize(
    "open_api__security",
    [LazyFixture(lambda security_requirement: [security_requirement])],
)
@pytest.mark.parametrize("open_api__tags", [LazyFixture(lambda tag: [tag])])
def test_openapi_full(open_api, info, security_requirement, tag):
    assert open_api.get_value() == {
        "openapi": "3.0.3",
        "info": info.get_value(),
        "servers": [],
        "paths": {},
        "components": {},
        "security": [security_requirement.get_value()],
        "tags": [tag.get_value()],
    }


def test_info(info):
    assert info.get_value() == {
        "title": "title",
        "version": "1.0.0",
    }


@pytest.mark.parametrize("info__description", ["description"])
@pytest.mark.parametrize("info__terms_of_service", ["terms_of_service"])
@pytest.mark.parametrize("info__contact", [LazyFixture("contact")])
@pytest.mark.parametrize("info__license", [LazyFixture("license")])
def test_info_full(info, contact, license):
    assert info.get_value() == {
        "title": "title",
        "version": "1.0.0",
        "description": "description",
        "termsOfService": "terms_of_service",
        "contact": contact.get_value(),
        "license": license.get_value(),
    }


def test_contact(contact):
    assert contact.get_value() == {}


@pytest.mark.parametrize("contact__name", ["name"])
@pytest.mark.parametrize("contact__url", ["url"])
@pytest.mark.parametrize("contact__email", ["email"])
def test_contact_full(contact):
    assert contact.get_value() == {
        "name": "name",
        "url": "url",
        "email": "email",
    }


def test_license(license):
    assert license.get_value() == {
        "name": license.name,
    }


@pytest.mark.parametrize("license__url", ["url"])
def test_license_full(license):
    assert license.get_value() == {
        "name": license.name,
        "url": "url",
    }


def test_server(server):
    assert server.get_value() == {"url": server.url}


@pytest.mark.parametrize("server__description", ["description"])
@pytest.mark.parametrize(
    "server__variables", [LazyFixture(lambda server_variable: {"key": server_variable})]
)
def test_server_full(server, server_variable):
    assert server.get_value() == {
        "url": server.url,
        "description": "description",
        "variables": {
            "key": server_variable.get_value(),
        },
    }


def test_server_variable(server_variable):
    assert server_variable.get_value() == {"default": "default"}


@pytest.mark.parametrize("server_variable__enum", [["enum"]])
@pytest.mark.parametrize("server_variable__description", ["description"])
def test_server_variable_full(server_variable):
    assert server_variable.get_value() == {
        "default": "default",
        "enum": ["enum"],
        "description": "description",
    }


def test_components(components):
    assert components.get_value() == {}


@pytest.mark.parametrize(
    "components__schemas", [LazyFixture(lambda schema: {"schema": schema})]
)
@pytest.mark.parametrize(
    "components__responses", [LazyFixture(lambda response: {"response": response})]
)
@pytest.mark.parametrize(
    "components__parameters", [LazyFixture(lambda parameter: {"parameter": parameter})]
)
@pytest.mark.parametrize(
    "components__examples", [LazyFixture(lambda example: {"example": example})]
)
@pytest.mark.parametrize(
    "components__request_bodies",
    [LazyFixture(lambda request_body: {"request_body": request_body})],
)
@pytest.mark.parametrize(
    "components__headers", [LazyFixture(lambda header: {"header": header})]
)
@pytest.mark.parametrize(
    "components__security_schemes",
    [LazyFixture(lambda security_scheme: {"security_scheme": security_scheme})],
)
@pytest.mark.parametrize(
    "components__links", [LazyFixture(lambda link: {"link": link})]
)
@pytest.mark.parametrize(
    "components__callbacks", [LazyFixture(lambda callback: {"callback": callback})]
)
def test_components_full(
    components,
    schema,
    response,
    parameter,
    example,
    request_body,
    header,
    security_scheme,
    link,
    callback,
):
    assert components.get_value() == {
        "schemas": {"schema": schema.get_value()},
        "responses": {"response": response.get_value()},
        "parameters": {"parameter": parameter.get_value()},
        "examples": {"example": example.get_value()},
        "request_bodies": {"request_body": request_body.get_value()},
        "headers": {"header": header.get_value()},
        "securitySchemes": {"security_scheme": security_scheme.get_value()},
        "links": {"link": link.get_value()},
        "callbacks": {"callback": callback.get_value()},
    }


def test_paths(paths):
    assert paths.get_value() == {}


def test_path_item(path_item):
    assert path_item.get_value() == {}


@pytest.mark.parametrize("path_item__ref", ["ref"])
@pytest.mark.parametrize("path_item__summary", ["summary"])
@pytest.mark.parametrize("path_item__description", ["description"])
@pytest.mark.parametrize("path_item__get", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__put", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__post", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__delete", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__options", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__head", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__patch", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__trace", [LazyFixture("operation")])
@pytest.mark.parametrize("path_item__servers", [LazyFixture(lambda server: [server])])
@pytest.mark.parametrize(
    "path_item__parameters", [LazyFixture(lambda parameter: [parameter])]
)
def test_path_item_full(path_item, operation, server, parameter):
    assert path_item.get_value() == {
        "$ref": "ref",
        "summary": "summary",
        "description": "description",
        "get": operation.get_value(),
        "put": operation.get_value(),
        "post": operation.get_value(),
        "delete": operation.get_value(),
        "options": operation.get_value(),
        "head": operation.get_value(),
        "patch": operation.get_value(),
        "trace": operation.get_value(),
        "servers": [server.get_value()],
        "parameters": [parameter.get_value()],
    }


def test_operation(operation):
    assert operation.get_value() == {}


@pytest.mark.parametrize("operation__summary", ["summary"])
@pytest.mark.parametrize("operation__description", ["description"])
@pytest.mark.parametrize("operation__tags", [["tag"]])
@pytest.mark.parametrize(
    "operation__external_docs", [LazyFixture("external_documentation")]
)
@pytest.mark.parametrize("operation__operation_id", ["operation_id"])
@pytest.mark.parametrize(
    "operation__callbacks", [LazyFixture(lambda callback: {"key": callback})]
)
@pytest.mark.parametrize(
    "operation__parameters", [LazyFixture(lambda parameter: [parameter])]
)
@pytest.mark.parametrize("operation__responses", [LazyFixture("responses")])
@pytest.mark.parametrize("operation__request_body", [LazyFixture("request_body")])
@pytest.mark.parametrize("operation__deprecated", [True])
@pytest.mark.parametrize(
    "operation__security",
    [LazyFixture(lambda security_requirement: [security_requirement])],
)
@pytest.mark.parametrize("operation__servers", [LazyFixture(lambda server: [server])])
def test_operation_full(
    operation,
    external_documentation,
    responses,
    request_body,
    callback,
    parameter,
    security_requirement,
    server,
    tag,
):
    assert operation.get_value() == {
        "summary": "summary",
        "description": "description",
        "externalDocs": external_documentation.get_value(),
        "tags": ["tag"],
        "operationId": "operation_id",
        "callbacks": {"key": callback.get_value()},
        "parameters": [parameter.get_value()],
        "requestBody": request_body.get_value(),
        "responses": responses.get_value(),
        "deprecated": True,
        "security": [security_requirement.get_value()],
        "servers": [server.get_value()],
    }


def test_external_documentation(external_documentation):
    assert external_documentation.get_value() == {
        "url": external_documentation.url,
    }


@pytest.mark.parametrize("external_documentation__description", ["description"])
def test_external_documentation_full(external_documentation):
    assert external_documentation.get_value() == {
        "url": external_documentation.url,
        "description": "description",
    }


def test_parameter(parameter):
    assert parameter.get_value() == {
        "in": "query",
        "name": "name",
        "required": True,
    }


@pytest.mark.parametrize("parameter__description", ["description"])
@pytest.mark.parametrize("parameter__schema", [LazyFixture("schema")])
@pytest.mark.parametrize("parameter__required", [False])
@pytest.mark.parametrize("parameter__deprecated", [True])
@pytest.mark.parametrize("parameter__allow_empty_value", [True])
def test_parameter_full(parameter, schema):
    assert parameter.get_value() == {
        "in": "query",
        "name": "name",
        "description": "description",
        "deprecated": True,
        "allowEmptyValue": True,
        "schema": schema.get_value(),
    }


def test_request_body(request_body):
    assert request_body.get_value() == {"content": {}}


@pytest.mark.parametrize("request_body__description", ["description"])
@pytest.mark.parametrize("request_body__required", [True])
def test_request_body_full(request_body):
    assert request_body.get_value() == {
        "content": {},
        "description": "description",
        "required": True,
    }


def test_media_type(media_type):
    assert media_type.get_value() == {}


@pytest.mark.parametrize("media_type__schema", [LazyFixture("schema")])
@pytest.mark.parametrize("media_type__example", ["example"])
def test_media_type_full(media_type, schema):
    assert media_type.get_value() == {
        "schema": schema.get_value(),
        "example": "example",
    }


@pytest.mark.parametrize(
    "media_type__examples", [LazyFixture(lambda example: {"key": example})]
)
def test_media_type_examples(media_type, example):
    assert media_type.get_value() == {
        "examples": {"key": example.get_value()},
    }


@pytest.mark.parametrize(
    "media_type__encoding", [LazyFixture(lambda encoding: {"key": encoding})]
)
def test_media_type_encoding(media_type, encoding):
    assert media_type.get_value() == {
        "encoding": {"key": encoding.get_value()},
    }


def test_encoding(encoding):
    assert encoding.get_value() == {"explode": True}


@pytest.mark.parametrize("encoding__content_type", ["content_type"])
@pytest.mark.parametrize(
    "encoding__headers", [LazyFixture(lambda header: {"key": header})]
)
@pytest.mark.parametrize("encoding__style", ["style"])
@pytest.mark.parametrize("encoding__explode", [False])
@pytest.mark.parametrize("encoding__allow_reserved", [True])
def test_encoding_full(encoding, header):
    assert encoding.get_value() == {
        "contentType": "content_type",
        "headers": {"key": header.get_value()},
        "style": "style",
        "allowReserved": True,
    }


@pytest.mark.parametrize(
    "responses__values", [LazyFixture(lambda response: {"key": response})]
)
def test_responses(responses, response):
    assert responses.get_value() == {"key": response.get_value()}


def test_response(response):
    assert response.get_value() == {"description": "description"}


def test_response_no_description():
    with pytest.raises(ValueError, match="Invalid description"):
        Response(description=None)


@pytest.mark.parametrize(
    "response__headers", [LazyFixture(lambda header: {"key": header})]
)
@pytest.mark.parametrize(
    "response__content", [LazyFixture(lambda media_type: {"key": media_type})]
)
@pytest.mark.parametrize("response__links", [LazyFixture(lambda link: {"key": link})])
def test_response_full(response, header, media_type, link):
    assert response.get_value() == {
        "description": "description",
        "headers": {"key": header.get_value()},
        "content": {"key": media_type.get_value()},
        "links": {"key": link.get_value()},
    }


@pytest.mark.parametrize(
    "callback__values", [LazyFixture(lambda path_item: {"key": path_item})]
)
def test_callback(callback, path_item):
    assert callback.get_value() == {"key": path_item.get_value()}


def test_example(example):
    assert example.get_value() == {}


@pytest.mark.parametrize("example__summary", ["summary"])
@pytest.mark.parametrize("example__description", ["description"])
@pytest.mark.parametrize("example__value", ["value"])
@pytest.mark.parametrize("example__external_value", ["external_value"])
def test_example_full(example):
    assert example.get_value() == {
        "summary": "summary",
        "description": "description",
        "value": "value",
        "externalValue": "external_value",
    }


def test_link(link):
    assert link.get_value() == {}


@pytest.mark.parametrize("link__operation_ref", ["operation_ref"])
@pytest.mark.parametrize("link__operation_id", ["operation_id"])
@pytest.mark.parametrize("link__parameters", [{"key": "value"}])
@pytest.mark.parametrize("link__request_body", ["request_body"])
@pytest.mark.parametrize("link__description", ["description"])
@pytest.mark.parametrize("link__server", [LazyFixture("server")])
def test_link_full(link, server):
    assert link.get_value() == {
        "operationRef": "operation_ref",
        "operationId": "operation_id",
        "parameters": {"key": "value"},
        "requestBody": "request_body",
        "description": "description",
        "server": server.get_value(),
    }


def test_header(header):
    assert header.get_value() == {"required": True}


@pytest.mark.parametrize("header__description", ["description"])
@pytest.mark.parametrize("header__required", [False])
@pytest.mark.parametrize("header__deprecated", [True])
@pytest.mark.parametrize("header__allow_empty_value", [True])
def test_header_full(header):
    assert header.get_value() == {
        "description": "description",
        "deprecated": True,
        "allowEmptyValue": True,
    }


def test_tag(tag):
    assert tag.get_value() == {"name": "tag"}


@pytest.mark.parametrize("tag__description", ["description"])
@pytest.mark.parametrize("tag__external_docs", [LazyFixture("external_documentation")])
def test_tag_full(tag, external_documentation):
    assert tag.get_value() == {
        "name": "tag",
        "description": "description",
        "externalDocs": external_documentation.get_value(),
    }


def test_reference(reference):
    assert reference.get_value() == {"$ref": "ref"}


@pytest.mark.parametrize("schema__required", [True, False])
@pytest.mark.parametrize("open_api__components", [LazyFixture("components")])
@pytest.mark.parametrize(
    "components__schemas", [LazyFixture(lambda schema: {"abc": schema})]
)
@pytest.mark.usefixtures("components")
def test_reference_from_schema(schema, open_api):
    reference = Reference.from_schema(schema_name="abc", schema=schema)
    assert reference.ref == "#/components/schemas/abc"
    assert reference.required == schema.required

    assert reference.get_schema(open_api) == schema


@pytest.mark.parametrize("is_required", [True, False])
def test_reference_from_response(is_required, open_api):
    reference = Reference.from_response(response_name="abc", required=is_required)
    assert reference.ref == "#/components/responses/abc"
    assert reference.required is is_required

    with pytest.raises(ValueError):
        reference.get_schema(open_api)


@pytest.mark.parametrize("is_required", [True, False])
def test_reference_from_parameter(is_required, open_api):
    reference = Reference.from_parameter(parameter_name="abc", required=is_required)
    assert reference.ref == "#/components/parameters/abc"
    assert reference.required is is_required

    with pytest.raises(ValueError):
        reference.get_schema(open_api)


@pytest.mark.parametrize("is_required", [True, False])
def test_reference_from_example(is_required, open_api):
    reference = Reference.from_example(example_name="abc", required=is_required)
    assert reference.ref == "#/components/examples/abc"
    assert reference.required is is_required

    with pytest.raises(ValueError):
        reference.get_schema(open_api)


@pytest.mark.parametrize("is_required", [True, False])
def test_reference_from_security_scheme(is_required, open_api):
    reference = Reference.from_security_scheme(
        security_scheme_name="abc", required=is_required
    )
    assert reference.ref == "#/components/securitySchemes/abc"
    assert reference.required is is_required

    with pytest.raises(ValueError):
        reference.get_schema(open_api)


def test_schema(schema):
    assert schema.get_value() == {}


@pytest.mark.parametrize("schema__title", ["title"])
@pytest.mark.parametrize("schema__multiple_of", [1])
@pytest.mark.parametrize("schema__maximum", [2])
@pytest.mark.parametrize("schema__exclusive_maximum", [True])
@pytest.mark.parametrize("schema__minimum", [3])
@pytest.mark.parametrize("schema__exclusive_minimum", [True])
@pytest.mark.parametrize("schema__max_length", [4])
@pytest.mark.parametrize("schema__min_length", [5])
@pytest.mark.parametrize("schema__pattern", ["pattern"])
@pytest.mark.parametrize("schema__max_items", [6])
@pytest.mark.parametrize("schema__min_items", [7])
@pytest.mark.parametrize("schema__unique_items", [8])
@pytest.mark.parametrize("schema__max_properties", [9])
@pytest.mark.parametrize("schema__min_properties", [10])
@pytest.mark.parametrize("schema__required", [False])
@pytest.mark.parametrize(
    "schema__enum", [LazyFixture(lambda second_schema: [second_schema])]
)
@pytest.mark.parametrize("schema__type", ["type"])
@pytest.mark.parametrize(
    "schema__all_of", [LazyFixture(lambda second_schema: [second_schema])]
)
@pytest.mark.parametrize(
    "schema__any_of", [LazyFixture(lambda second_schema: [second_schema])]
)
@pytest.mark.parametrize(
    "schema__one_of", [LazyFixture(lambda second_schema: [second_schema])]
)
@pytest.mark.parametrize("schema__not_", [LazyFixture("second_schema")])
@pytest.mark.parametrize("schema__items", [LazyFixture("second_schema")])
@pytest.mark.parametrize(
    "schema__properties", [LazyFixture(lambda second_schema: {"key": second_schema})]
)
@pytest.mark.parametrize(
    "schema__additional_properties", [LazyFixture("second_schema")]
)
@pytest.mark.parametrize("schema__description", ["description"])
@pytest.mark.parametrize("schema__format", ["format"])
@pytest.mark.parametrize("schema__default", ["default"])
@pytest.mark.parametrize("schema__example", ["example"])
@pytest.mark.parametrize("schema__discriminator", [LazyFixture("discriminator")])
def test_schema_full(schema, second_schema, discriminator):
    schema.options = {"abc": "def"}

    assert schema.get_value() == {
        "additionalProperties": second_schema.get_value(),
        "allOf": [{}],
        "anyOf": [{}],
        "default": "default",
        "description": "description",
        "discriminator": discriminator.get_value(),
        "enum": [second_schema.get_value()],
        "example": "example",
        "exclusiveMaximum": True,
        "exclusiveMinimum": True,
        "format": "format",
        "items": {},
        "maxItems": 6,
        "maxLength": 4,
        "maxProperties": 9,
        "maximum": 2,
        "minItems": 7,
        "minLength": 5,
        "minProperties": 10,
        "minimum": 3,
        "multipleOf": 1,
        "not": second_schema.get_value(),
        "oneOf": [{}],
        "pattern": "pattern",
        "properties": {"key": {}},
        "required": ["key"],
        "title": "title",
        "type": "type",
        "uniqueItems": 8,
        "abc": "def",
    }


@pytest.mark.parametrize(
    "schema__examples", [LazyFixture(lambda example: {"key": example})]
)
def test_schema_examples(schema, example):
    assert schema.get_value() == {"examples": {"key": example.get_value()}}


@pytest.mark.parametrize("schema__example", ["example"])
@pytest.mark.parametrize(
    "schema__examples", [LazyFixture(lambda example: {"key": example})]
)
def test_schema_example_and_examples(schema, example):
    with pytest.raises(
        ValueError, match="`example` and `examples` are mutually exclusive"
    ):
        schema.get_value()


def test_discriminator(discriminator):
    assert discriminator.get_value() == {"propertyName": "property_name"}


@pytest.mark.parametrize("discriminator__mapping", [{"key": "value"}])
def test_discriminator_full(discriminator):
    assert discriminator.get_value() == {
        "propertyName": "property_name",
        "mapping": {"key": "value"},
    }


def test_security_scheme(security_scheme):
    assert security_scheme.get_value() == {
        "in": "query",
        "type": "http",
    }


@pytest.mark.parametrize("security_scheme__name", ["name"])
@pytest.mark.parametrize("security_scheme__scheme", ["scheme"])
@pytest.mark.parametrize(
    "security_scheme__flows", [LazyFixture(lambda oauth_flow: [oauth_flow])]
)
@pytest.mark.parametrize(
    "security_scheme__open_id_connect_url", ["open_id_connect_url"]
)
@pytest.mark.parametrize("security_scheme__description", ["description"])
@pytest.mark.parametrize("security_scheme__bearer_format", ["bearer_format"])
def test_security_scheme_full(security_scheme, oauth_flow):
    assert security_scheme.get_value() == {
        "in": "query",
        "type": "http",
        "name": "name",
        "scheme": "scheme",
        "flows": [oauth_flow.get_value()],
        "openIdConnectUrl": "open_id_connect_url",
        "description": "description",
        "bearerFormat": "bearer_format",
    }


def test_oauth_flows(oauth_flows):
    assert oauth_flows.get_value() == {}


@pytest.mark.parametrize("oauth_flows__implicit", [LazyFixture("oauth_flow")])
@pytest.mark.parametrize("oauth_flows__password", [LazyFixture("oauth_flow")])
@pytest.mark.parametrize("oauth_flows__client_credentials", [LazyFixture("oauth_flow")])
@pytest.mark.parametrize("oauth_flows__authorization_code", [LazyFixture("oauth_flow")])
def test_oauth_flows_full(oauth_flows, oauth_flow):
    assert oauth_flows.get_value() == {
        "implicit": oauth_flow.get_value(),
        "password": oauth_flow.get_value(),
        "clientCredentials": oauth_flow.get_value(),
        "authorizationCode": oauth_flow.get_value(),
    }


def test_oauth_flow(oauth_flow):
    assert oauth_flow.get_value() == {
        "authorizationUrl": oauth_flow.authorization_url,
        "scopes": {},
        "tokenUrl": oauth_flow.token_url,
    }


@pytest.mark.parametrize("oauth_flow__refresh_url", ["refresh_url"])
@pytest.mark.parametrize("oauth_flow__scopes", [{"key": "value"}])
def test_oauth_flow_full(oauth_flow):
    assert oauth_flow.get_value() == {
        "authorizationUrl": oauth_flow.authorization_url,
        "scopes": {"key": "value"},
        "tokenUrl": oauth_flow.token_url,
        "refreshUrl": "refresh_url",
    }


def test_security_requirement(security_requirement):
    assert security_requirement.get_value() == {}
