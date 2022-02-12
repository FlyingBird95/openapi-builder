import pytest

from openapi_builder import DocumentationOptions
from openapi_builder.documentation import Documentation
from openapi_builder.exceptions import MissingConfigContext, MissingConverter
from openapi_builder.specification import Schema


@pytest.mark.parametrize(
    "documentation_options__strict_mode",
    [DocumentationOptions.StrictMode.FAIL_ON_ERROR],
)
def test_strict_mode_error(open_api_documentation):
    builder = open_api_documentation.builder
    with pytest.raises(MissingConverter):
        with builder.config_manager.use_documentation_context(Documentation()):
            open_api_documentation.builder.schema_manager.process(None, name="abc")


@pytest.mark.parametrize(
    "documentation_options__strict_mode",
    [DocumentationOptions.StrictMode.SHOW_WARNINGS],
)
def test_strict_mode_warning(open_api_documentation):
    builder = open_api_documentation.builder
    with builder.config_manager.use_documentation_context(Documentation()):
        result = open_api_documentation.builder.schema_manager.process(None, name="abc")

    assert isinstance(result, Schema)
    assert result.example == "<unknown>"


@pytest.mark.parametrize("documentation_options__strict_mode", [None])
def test_unknown_strict_mode(open_api_documentation):
    builder = open_api_documentation.builder
    with pytest.raises(ValueError):
        with builder.config_manager.use_documentation_context(Documentation()):
            open_api_documentation.builder.schema_manager.process(None, name="abc")


def test_unknown_documentation(open_api_documentation):
    builder = open_api_documentation.builder
    with pytest.raises(TypeError):
        with builder.config_manager.use_documentation_context(None):
            open_api_documentation.builder.process()


def test_missing_context(open_api_documentation):
    with pytest.raises(MissingConfigContext):
        open_api_documentation.builder.config_manager.ensure_valid_config()
