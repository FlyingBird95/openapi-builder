from openapi_builder import OpenApiDocumentation


def test_configuring_flask_app_option_1(http):
    """Test configuring the app according to option 1 is supported."""
    app = http.application
    documentation = OpenApiDocumentation(app=app)
    assert documentation.app == app
    assert app.extensions["__open_api_doc__"] == documentation
    assert documentation.builder.iterate_endpoints in app.before_first_request_funcs


def test_configuring_flask_app_option_2(http):
    """Test configuring the app according to option 2 is supported."""
    app = http.application
    documentation = OpenApiDocumentation()
    documentation.init_app(app=app)
    assert documentation.app == app
    assert app.extensions["__open_api_doc__"] == documentation
    assert documentation.builder.iterate_endpoints in app.before_first_request_funcs
