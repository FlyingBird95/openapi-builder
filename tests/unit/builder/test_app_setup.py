import pytest

from openapi_builder import OpenApiDocumentation


def test_configuring_flask_app_option_1(app):
    """Test configuring the app according to option 1 is supported."""
    documentation = OpenApiDocumentation(app=app)
    assert documentation.app == app
    assert app.extensions["__open_api_doc__"] == documentation


def test_configuring_flask_app_option_2(app):
    """Test configuring the app according to option 2 is supported."""
    documentation = OpenApiDocumentation()
    documentation.init_app(app=app)
    assert documentation.app == app
    assert app.extensions["__open_api_doc__"] == documentation


@pytest.mark.parametrize("app", [None, {}])
def test_configuring_flask_app_no_flask(app):
    documentation = OpenApiDocumentation()
    with pytest.raises(TypeError):
        documentation.init_app(app=app)
