from http import HTTPStatus

import halogen
import pytest
from flask import jsonify
from halogen import Schema

from openapi_builder import add_documentation, set_schema_options
from openapi_builder.documentation import DiscriminatorOptions


@pytest.fixture
def documentation_options__include_halogen_converters():
    return True


@pytest.fixture
def documentation_options__include_marshmallow_converters():
    return False


@pytest.mark.usefixtures("get_with_halogen_schema")
def test_get_halogen_string_schema(
    http, halogen_schema, second_halogen_schema, open_api_documentation
):
    set_schema_options(
        schema=halogen_schema,
        discriminator=DiscriminatorOptions(
            name="discriminator_options",
            all_of=True,
            mapping={"second": second_halogen_schema},
        ),
    )
    response = http.get("/get_with_halogen_schema")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"field": "value"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_halogen_schema"]
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


@pytest.mark.usefixtures("get_with_halogen_schema")
def test_halogen_description_from_docstring(http, app, open_api_documentation):
    """Test that a schema attribute docstring is used as a description."""

    class Fish(Schema):
        name = halogen.Attr(halogen.types.String())
        name.__doc__ = "Name of this fish."

    @app.route("/fish", methods=["POST"])
    @add_documentation(request_data=Fish)
    def post_fish():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    assert configuration["paths"]["/fish"]["post"]["requestBody"]["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Fish"}}
    }

    fish_schema = configuration["components"]["schemas"]["Fish"]
    assert fish_schema["type"] == "object"
    assert fish_schema["required"] == ["name"]
    assert fish_schema["properties"] == {"name": {"type": "string", "description": "Name of this fish."}}


@pytest.mark.usefixtures("get_with_halogen_schema")
def test_halogen_description_from_docstring_hidden(http, app, open_api_documentation):
    """Test that internal docstrings are not used in public descriptions."""

    class FishWithSecrets(Schema):
        """Schema with internal docs on fields."""

        @halogen.attr(halogen.types.String())
        def nickname(value):
            """Docstring explaining an internal implementation detail."""
            return value

        @halogen.attr(halogen.types.String())
        def num_fins(value):
            """Docstring explaining an internal implementation detail."""
            return value
        num_fins.__doc__ = "Public doc."

    @app.route("/fish", methods=["GET"])
    @add_documentation(response=FishWithSecrets)
    def get_fish():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()

    fish_schema = configuration["components"]["schemas"]["FishWithSecrets"]
    assert fish_schema["required"] == ["nickname", "num_fins"]
    assert fish_schema["properties"]["nickname"] == {"type": "string"}
    assert fish_schema["properties"]["num_fins"] == {"type": "string", "description": "Public doc."}
