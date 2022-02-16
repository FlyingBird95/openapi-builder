from http import HTTPStatus

import pytest

from openapi_builder.converters.schema import halogen, marshmallow


def test_register_marshmallow_converters(open_api_documentation):
    """Test that marshmallow converters are registered by default."""
    # open_api_documentation = OpenApiDocumentation(app=app)
    open_api_documentation.app.try_trigger_before_first_request_functions()
    assert any(
        isinstance(converter, marshmallow.StringConverter)
        for converter in open_api_documentation.builder.schema_manager.converters
    )


@pytest.mark.parametrize("documentation_options__include_halogen_converters", [True])
@pytest.mark.parametrize(
    "documentation_options__include_marshmallow_converters", [False]
)
def test_register_halogen_converters(http, open_api_documentation):
    """Test that halogen converters can be registered."""
    open_api_documentation.app.try_trigger_before_first_request_functions()
    assert any(
        isinstance(converter, halogen.StringConverter)
        for converter in open_api_documentation.builder.schema_manager.converters
    )


@pytest.mark.usefixtures("get_without_decorator")
def test_get_without_decorator(http, open_api_documentation):
    response = http.get("/get_without_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_specification()
    assert configuration["paths"] == {}


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_head_response", [True])
@pytest.mark.parametrize("documentation_options__include_options_response", [True])
def test_get_with_decorator(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert path["head"] == {"responses": {}}
    assert path["options"] == {"responses": {}}


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_head_response", [False])
def test_get_with_decorator_no_head(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert "head" not in path


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_options_response", [False])
def test_get_with_decorator_no_options(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert "options" not in path


@pytest.mark.usefixtures("get_with_marshmallow_schema")
@pytest.mark.parametrize(
    "documentation_options__response_content_type", ["something-else"]
)
def test_response_content_type(http, open_api_documentation):
    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_marshmallow_schema"]
    responses = path["get"]["responses"]
    assert "something-else" in responses["200"]["content"]


@pytest.mark.usefixtures("post_with_marshmallow_request_data")
@pytest.mark.parametrize(
    "documentation_options__request_content_type", ["something-else"]
)
def test_request_content_type(http, open_api_documentation):
    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/post_with_marshmallow_request_data"]
    request_body = path["post"]["requestBody"]
    assert "something-else" in request_body["content"]


@pytest.mark.usefixtures("put_with_marshmallow_request_query")
def test_query_options(http, open_api_documentation):
    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/put_with_marshmallow_request_query"]
    [parameter] = path["put"]["parameters"]
    assert parameter["in"] == "query"
    assert parameter["name"] == "field"
    assert parameter["schema"] == {"type": "string"}
    assert path["put"]["responses"] == {}
