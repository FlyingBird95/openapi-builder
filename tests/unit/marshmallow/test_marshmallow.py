from http import HTTPStatus

import pytest


@pytest.mark.usefixtures("get_with_marshmallow_schema")
def test_get_marshmallow_string_schema(http, open_api_documentation):
    response = http.get("/get_with_marshmallow_schema")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"field": "value"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/get_with_marshmallow_schema"]
    operation = path["get"]["responses"]["200"]
    assert operation["description"] is None
    ref = operation["content"]["application/json"]["schema"]
    assert ref == {"$ref": "#/components/schemas/GeneratedSchema"}

    schema = configuration["components"]["schemas"]["GeneratedSchema"]
    assert schema["type"] == "object"
    assert schema["properties"] == {"field": {"type": "string", "format": "string"}}
