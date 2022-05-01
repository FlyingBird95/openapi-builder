from http import HTTPStatus

import pytest

from openapi_builder import set_resource_options, set_schema_options
from openapi_builder.converters.schema.halogen import SchemaConverter
from openapi_builder.documentation import DiscriminatorOptions
from openapi_builder.specification import Tag


@pytest.mark.usefixtures("get_user_with_decorator")
def test_set_resource_options(http, app, user_blueprint, open_api_documentation):
    app.register_blueprint(user_blueprint)
    set_resource_options(user_blueprint, tags=[Tag(name="user-tag")])

    response = http.get("/users/get_user")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"user": "abc"}

    configuration = open_api_documentation.get_specification()
    path = configuration["paths"]["/users/get_user"]
    assert path["get"] == {"tags": ["user-tag"], "responses": {}}
