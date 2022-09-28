from http import HTTPStatus

import pytest
from flask import jsonify
import marshmallow

from openapi_builder import add_documentation
from openapi_builder.converters.schema import (
    halogen as halogen_converters,
    marshmallow as marshmallow_converters,
)


def test_register_marshmallow_converters(open_api_documentation):
    """Test that marshmallow converters are registered by default."""
    # open_api_documentation = OpenApiDocumentation(app=app)
    open_api_documentation.app.try_trigger_before_first_request_functions()
    assert any(
        isinstance(converter, marshmallow_converters.StringConverter)
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
        isinstance(converter, halogen_converters.StringConverter)
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


@pytest.mark.parametrize(
    "documentation_options__response_content_type", ["something-else"]
)
def test_response_content_type(http, app, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(
        {
            "field": marshmallow.fields.String(),
        }
    )

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get"]
    responses = path["get"]["responses"]
    assert "something-else" in responses["200"]["content"]


@pytest.mark.parametrize(
    "documentation_options__request_content_type", ["something-else"]
)
def test_request_content_type(http, app, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(
        {
            "field": marshmallow.fields.String(),
        }
    )

    @app.route("/post", methods=["POST"])
    @add_documentation(request_data=marshmallow_schema)
    def post():
        return jsonify({"status": "OK"})

    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/post"]
    request_body = path["post"]["requestBody"]
    assert "something-else" in request_body["content"]


def test_query_options(http, app, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(
        {
            "field": marshmallow.fields.String(),
        }
    )

    @app.route("/put", methods=["PUT"])
    @add_documentation(request_query=marshmallow_schema)
    def put():
        return jsonify({"status": "OK"})

    open_api_documentation.app.try_trigger_before_first_request_functions()
    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/put"]
    [parameter] = path["put"]["parameters"]
    assert parameter["in"] == "query"
    assert parameter["name"] == "field"
    assert parameter["schema"] == {"type": "string"}
    assert path["put"]["responses"] == {}
