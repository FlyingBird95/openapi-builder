import marshmallow
import pytest
from flask import jsonify

from openapi_builder import add_documentation


@pytest.fixture
def route_with_parameter():
    return "/<route>"


@pytest.fixture
def get_with_route_validator(app, route_with_parameter):
    marshmallow_schema = marshmallow.Schema.from_dict(
        {
            "field": marshmallow.fields.String(),
        }
    )

    @app.route(route_with_parameter, methods=["GET"])
    @add_documentation(response=marshmallow_schema())
    def get(route):
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    return get


@pytest.mark.parametrize(
    "route_with_parameter, expected_schema",
    [
        ("/<string:route>", {"type": "string", "format": "string"}),
        ("/<any:route>", {"type": "string", "format": "string"}),
        ("/<path:route>", {"type": "string", "format": "string"}),
        ("/<int:route>", {"type": "number", "format": "integer"}),
        ("/<float:route>", {"type": "number", "format": "float"}),
        ("/<uuid:route>", {"type": "string", "format": "hex"}),
    ],
)
@pytest.mark.usefixtures("get_with_route_validator")
def test_parameter_converter(http, open_api_documentation, expected_schema):
    http.get("/get_with_route_validator")

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/{route}"]
    [parameter] = path["parameters"]
    assert parameter["in"] == "path"
    assert parameter["name"] == "route"
    assert parameter["required"] is True
    assert parameter["schema"] == expected_schema
