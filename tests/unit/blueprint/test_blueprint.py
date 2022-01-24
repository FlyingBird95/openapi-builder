from http import HTTPStatus

import pytest
from werkzeug.routing import BuildError


@pytest.mark.usefixtures("open_api_documentation")
def test_get(http):
    response = http.get(http.make_uri("openapi_documentation.get"))

    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/html"


@pytest.mark.parametrize(
    "documentation_options__include_documentation_blueprint", [False]
)
@pytest.mark.parametrize(
    "endpoint",
    [
        "openapi_documentation.get",
        "openapi_documentation.specification",
    ],
)
@pytest.mark.usefixtures("open_api_documentation")
def test_blueprint_not_included(http, endpoint):
    with pytest.raises(BuildError):
        http.make_uri(endpoint)


@pytest.mark.usefixtures("open_api_documentation")
def test_specification(http):
    response = http.get(http.make_uri("openapi_documentation.specification"))

    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "application/json"

    data = response.parsed_data
    assert "components" in data
    assert "info" in data
    assert "title" in data["info"]
    assert "version" in data["info"]
    assert "openapi" in data
    assert "paths" in data
    assert "servers" in data
