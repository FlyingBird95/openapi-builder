from http import HTTPStatus

import halogen
import pytest
from flask import jsonify

from openapi_builder import add_documentation, set_schema_options
from openapi_builder.documentation import DiscriminatorOptions


class Fish(halogen.Schema):
    """Fish class."""

    name = halogen.Attr(halogen.types.String())
    """Name of this fish."""


@pytest.fixture
def documentation_options__include_halogen_converters():
    return True


@pytest.fixture
def documentation_options__include_marshmallow_converters():
    return False


def test_get_halogen_string_schema(http, app, open_api_documentation):
    halogen_schema = halogen.Schema(
        field=halogen.Attr(halogen.types.String()),
    )
    second_halogen_schema = halogen.Schema(
        field=halogen.Attr(halogen.types.Int()),
    )

    @app.route("/get")
    @add_documentation(response=halogen_schema)
    def get():
        return jsonify(halogen_schema.serialize({"field": "value"}))

    set_schema_options(
        schema=halogen_schema,
        discriminator=DiscriminatorOptions(
            name="discriminator_options",
            all_of=True,
            mapping={"second": second_halogen_schema},
        ),
    )
    response = http.get("/get")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"field": "value"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get"]
    operation = path["get"]["responses"]["200"]
    assert operation["description"] == ""
    ref = operation["content"]["application/json"]["schema"]
    assert ref == {"$ref": "#/components/schemas/Schema"}

    schema = configuration["components"]["schemas"]["Schema"]
    assert schema["type"] == "object"
    assert schema["discriminator"]["mapping"] == {
        "second": "#/components/schemas/Schema"
    }
    assert schema["discriminator"]["propertyName"] == "discriminator_options"
    assert schema["oneOf"] == [{"$ref": "#/components/schemas/Schema"}]

    [all_of] = schema["allOf"]
    assert all_of["type"] == "object"
    assert all_of["properties"] == {"field": {"type": "string"}}
    assert all_of["required"] == ["field"]
