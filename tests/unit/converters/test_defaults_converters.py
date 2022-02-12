import enum

import pytest
from marshmallow import fields


@pytest.mark.parametrize(
    "marshmallow_fields",
    [
        {"field": fields.String(dump_default="abc")},
        {"field": fields.String(load_default="abc")},
    ],
)
@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_vanilla_converter(http, open_api_documentation):
    http.get("/get_with_marshmallow_schema")

    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "abc"}


@pytest.mark.parametrize(
    "marshmallow_fields", [{"field": fields.List(fields.String(), dump_default=[])}]
)
@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_list_converter(http, open_api_documentation):
    http.get("/get_with_marshmallow_schema")

    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "array", "default": []}


@pytest.mark.parametrize(
    "marshmallow_fields", [{"field": fields.String(dump_default=lambda: "abc")}]
)
@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_callable_converter(http, open_api_documentation):
    http.get("/get_with_marshmallow_schema")

    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "abc"}


class MyEnum(enum.Enum):
    first_value = "first_value"
    second_value = "second_value"


@pytest.mark.parametrize(
    "marshmallow_fields", [{"field": fields.String(dump_default=MyEnum.first_value)}]
)
@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_enum_converter(http, open_api_documentation):
    http.get("/get_with_marshmallow_schema")

    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string", "default": "first_value"}


@pytest.mark.parametrize(
    "marshmallow_fields", [{"field": fields.String(dump_default=None)}]
)
@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_none_converter(http, open_api_documentation):
    http.get("/get_with_marshmallow_schema")

    configuration = open_api_documentation.get_specification()
    properties = configuration["components"]["schemas"]["GeneratedSchema"]["properties"]
    assert properties["field"] == {"type": "string"}
