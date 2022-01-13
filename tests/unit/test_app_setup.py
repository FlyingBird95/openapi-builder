from openapi_builder import OpenApiDocumentation
from openapi_builder.converters.marshmallow import StringConverter


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


def test_default_options(app):
    """Test default options for the OpenApiDocumentation."""
    open_api_documentation = OpenApiDocumentation(app=app)
    configuration = open_api_documentation.get_specification()
    info = configuration["info"]
    assert info["title"] == "Open API REST documentation"
    assert info["version"] == "1.0.0"

    assert configuration["openapi"] == "3.0.3"
    assert configuration["servers"] == [{"url": "/"}]

    options = open_api_documentation.options
    assert options.include_head_response is True
    assert options.include_options_response is True
    assert options.include_marshmallow_converters is True
    assert options.include_documentation_blueprint is True


def test_register_marshmallow_converters(app):
    """Test that marshmallow converters are registered by default."""
    open_api_documentation = OpenApiDocumentation(app=app)
    app.try_trigger_before_first_request_functions()
    assert any(
        isinstance(converter, StringConverter)
        for converter in open_api_documentation.builder.converters
    )
