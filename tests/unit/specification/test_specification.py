# TODO: The tests below are only checking if the 'get_value' returns the correct value, but the
#  input is based on the test-setup, so they're not very useful.


def test_openapi(open_api, info):
    assert open_api.get_value() == {
        "openapi": "3.0.3",
        "info": info.get_value(),
        "servers": [],
        "paths": {},
        "components": {},
    }


def test_info(info, contact, license):
    assert info.get_value() == {
        "title": "title",
        "version": "1.0.0",
        "description": "description",
        "termsOfService": "terms_of_service",
        "contact": contact.get_value(),
        "license": license.get_value(),
    }


def test_contact(contact):
    assert contact.get_value() == {"email": "email", "name": "name", "url": contact.url}


def test_license(license):
    assert license.get_value() == {
        "name": "name",
        "url": license.url,
    }


def test_server(server):
    assert server.get_value() == {"description": "description", "url": "/"}


def test_server_variable(server_variable):
    assert server_variable.get_value() == {"default": None}


def test_components(components):
    assert components.get_value() == {}


def test_paths(paths):
    assert paths.get_value() == {}


def test_path_item(path_item):
    assert path_item.get_value() == {}


def test_operation(operation):
    assert operation.get_value() == {}


def test_external_documentation(external_documentation):
    assert external_documentation.get_value() == {
        "description": "description",
        "url": external_documentation.url,
    }


def test_parameter(parameter):
    assert parameter.get_value() == {
        "in": "query",
        "name": "name",
        "required": True,
    }


def test_request_body(request_body):
    assert request_body.get_value() == {"content": {}}


def test_media_type(media_type):
    assert media_type.get_value() == {}


def test_encoding(encoding):
    assert encoding.get_value() == {"explode": True}


def test_responses(responses):
    assert responses.get_value() == {}


def test_response(response):
    assert response.get_value() == {"description": "description"}


def test_callback(callback):
    assert callback.get_value() == {}


def test_example(example):
    assert example.get_value() == {}


def test_link(link):
    assert link.get_value() == {}


def test_header(header):
    assert header.get_value() == {"required": True}


def test_tag(tag):
    assert tag.get_value() == {"name": "tag"}


def test_reference(reference):
    assert reference.get_value() == {"$ref": "ref"}


def test_schema(schema):
    assert schema.get_value() == {}


def test_discriminator(discriminator):
    assert discriminator.get_value() == {"propertyName": "property_name"}


def test_security_scheme(security_scheme):
    assert security_scheme.get_value() == {
        "in": "query",
        "name": "name",
        "openIdConnectUrl": security_scheme.open_id_connect_url,
        "scheme": "scheme",
        "type": "http",
    }


def test_o_auth_flows(o_auth_flows):
    assert o_auth_flows.get_value() == {}


def test_o_auth_flow(o_auth_flow):
    assert o_auth_flow.get_value() == {
        "authorizationUrl": o_auth_flow.authorization_url,
        "scopes": {},
        "tokenUrl": o_auth_flow.token_url,
    }


def test_security_requirement(security_requirement):
    assert security_requirement.get_value() == {}
