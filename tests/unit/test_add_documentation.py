from http import HTTPStatus

import pytest


@pytest.mark.usefixtures("get_without_decorator")
def test_get_without_decorator(http, open_api_documentation):
    response = http.get("/get_without_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_configuration()
    assert configuration["paths"] == {}


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_head_response", [True])
@pytest.mark.parametrize("documentation_options__include_options_response", [True])
def test_get_with_decorator(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_configuration()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert path["head"] == {"responses": {}}
    assert path["options"] == {"responses": {}}


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_head_response", [False])
def test_get_with_decorator_no_head(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_configuration()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert "head" not in path


@pytest.mark.usefixtures("get_with_decorator")
@pytest.mark.parametrize("documentation_options__include_options_response", [False])
def test_get_with_decorator_no_options(http, open_api_documentation):
    response = http.get("/get_with_decorator")
    assert response.status_code == HTTPStatus.OK
    assert response.parsed_data == {"status": "OK"}

    configuration = open_api_documentation.get_configuration()
    path = configuration["paths"]["/get_with_decorator"]
    assert path["get"] == {"responses": {}}
    assert "options" not in path
