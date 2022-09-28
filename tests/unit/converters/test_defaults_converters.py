import enum

import pytest
import marshmallow
from flask import jsonify

from openapi_builder import add_documentation


@pytest.mark.parametrize(
    "marshmallow_fields",
    [
        {"field": marshmallow.fields.String(dump_default="abc")},
        {"field": marshmallow.fields.String(load_default="abc")},
    ],
)
def test_vanilla_converter(http, app, marshmallow_fields, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(marshmallow_fields)

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    http.get("/get")
    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "abc"}


@pytest.mark.parametrize(
    "marshmallow_fields",
    [{"field": marshmallow.fields.List(marshmallow.fields.String(), dump_default=[])}],
)
def test_list_converter(http, app, marshmallow_fields, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(marshmallow_fields)

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    http.get("/get")
    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "array", "default": []}


@pytest.mark.parametrize(
    "marshmallow_fields",
    [{"field": marshmallow.fields.String(dump_default=lambda: "abc")}],
)
def test_callable_converter(http, app, marshmallow_fields, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(marshmallow_fields)

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    http.get("/get")
    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "abc"}


class MyEnum(enum.Enum):
    first_value = "first_value"
    second_value = "second_value"


@pytest.mark.parametrize(
    "marshmallow_fields",
    [{"field": marshmallow.fields.String(dump_default=MyEnum.first_value)}],
)
def test_enum_converter(http, app, marshmallow_fields, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(marshmallow_fields)

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    http.get("/get")
    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "first_value"}


@pytest.mark.parametrize(
    "marshmallow_fields", [{"field": marshmallow.fields.String(dump_default=None)}]
)
def test_none_converter(http, app, marshmallow_fields, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(marshmallow_fields)

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    http.get("/get")
    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": None}
