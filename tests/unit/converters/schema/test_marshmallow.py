from http import HTTPStatus

import marshmallow
from flask import jsonify

from openapi_builder import add_documentation


def test_get_marshmallow_string_schema(http, app, open_api_documentation):
    marshmallow_schema = marshmallow.Schema.from_dict(
        {
            "field": marshmallow.fields.String(),
        },
    )

    @app.route("/get")
    @add_documentation(response=marshmallow_schema())
    def get():
        return jsonify(marshmallow_schema().dump({"field": "value"}))

    response = http.get("/get")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"field": "value"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get"]
    operation = path["get"]["responses"]["200"]
    assert operation["description"] == ""
    ref = operation["content"]["application/json"]["schema"]
    assert ref == {"$ref": "#/components/schemas/GeneratedSchema"}

    schema = configuration["components"]["schemas"]["GeneratedSchema"]
    assert schema["type"] == "object"
    assert schema["properties"] == {"field": {"type": "string"}}
