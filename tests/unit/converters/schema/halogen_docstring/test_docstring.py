import pytest
from flask import jsonify

from openapi_builder import add_documentation
from .cat import Cat
from .dog import Dog
from .fish import Fish
from .snake import Snake, Python


@pytest.fixture
def documentation_options__include_halogen_converters():
    return True


@pytest.fixture
def documentation_options__include_marshmallow_converters():
    return False


def test_fish(http, app, open_api_documentation):
    """Test that a schema attribute docstring is used as a description."""

    @app.route("/fish", methods=["POST"])
    @add_documentation(request_data=Fish)
    def post():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    assert configuration["paths"]["/fish"]["post"]["requestBody"]["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Fish"}}
    }

    fish_schema = configuration["components"]["schemas"]["Fish"]
    assert fish_schema["description"] == "Fish schema."
    assert fish_schema["type"] == "object"
    assert fish_schema["required"] == ["name", "age"]
    assert fish_schema["properties"] == {
        "name": {"type": "string", "description": "The name of the fish."},
        "age": {"type": "integer", "description": "The age of the fish in years."},
    }


def test_cat(http, app, open_api_documentation):
    """Test that a schema attribute docstring is used as a description."""

    @app.get("/cat")
    @add_documentation(response=Cat)
    def get():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    response = configuration["paths"]["/cat"]["get"]["responses"]["200"]
    assert response["description"] == ""
    assert response["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Cat"}}
    }

    cat_schema = configuration["components"]["schemas"]["Cat"]
    assert cat_schema["description"] == "Cat schema."
    assert cat_schema["type"] == "object"
    assert cat_schema["required"] == ["name", "age"]
    assert cat_schema["properties"] == {
        "name": {"type": "string", "description": "The name of the cat."},
        "age": {"type": "integer", "description": "The age of the cat in years."},
    }


def test_dog(http, app, open_api_documentation):
    """Test that a schema attribute docstring is used as a description."""

    @app.get("/dog")
    @add_documentation(response=Dog)
    def get():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    response = configuration["paths"]["/dog"]["get"]["responses"]["200"]
    assert response["description"] == ""
    assert response["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Dog"}}
    }

    cat_schema = configuration["components"]["schemas"]["Dog"]
    assert cat_schema["description"] == "Dog schema."
    assert cat_schema["type"] == "object"
    assert cat_schema["required"] == ["num_legs", "name", "age"]
    assert cat_schema["properties"] == {
        "name": {"type": "string", "description": "The name of the dog."},
        "age": {"type": "integer", "description": "The age of the dog in years."},
        "num_legs": {
            "description": "Number of legs for this animal.",
            "type": "integer",
        },
    }


def test_snake(http, app, open_api_documentation):
    """Test that a schema attribute docstring is used as a description."""

    @app.put("/snake")
    @add_documentation(response=Snake)
    def put():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    response = configuration["paths"]["/snake"]["put"]["responses"]["200"]
    assert response["description"] == ""
    assert response["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Snake"}}
    }

    snake_schema = configuration["components"]["schemas"]["Snake"]
    assert snake_schema["description"] == "Snake schema."
    assert snake_schema["type"] == "object"
    assert snake_schema["required"] == ["name", "age", "length"]
    assert snake_schema["properties"] == {
        "name": {"type": "string", "description": "The name of the animal."},
        "age": {"type": "integer", "description": "The age of the animal in years."},
        "length": {"type": "integer"},
    }


def test_python(http, app, open_api_documentation):
    """Test schema with double inheritance."""

    @app.put("/python")
    @add_documentation(response=Python)
    def put():
        return jsonify({})

    app.try_trigger_before_first_request_functions()

    configuration = open_api_documentation.get_specification()
    response = configuration["paths"]["/python"]["put"]["responses"]["200"]
    assert response["description"] == ""
    assert response["content"] == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Python"}}
    }

    snake_schema = configuration["components"]["schemas"]["Python"]
    assert (
        snake_schema["description"] == "Python schema for testing double inheritance."
    )
    assert snake_schema["type"] == "object"
    assert snake_schema["required"] == ["name", "age", "length", "is_dangerous"]
    assert snake_schema["properties"] == {
        "name": {"type": "string", "description": "The name of the animal."},
        "age": {"type": "integer", "description": "The age of the animal in years."},
        "length": {"type": "integer"},
        "is_dangerous": {
            "type": "boolean",
            "description": "Whether this Python is dangerous.",
        },
    }
