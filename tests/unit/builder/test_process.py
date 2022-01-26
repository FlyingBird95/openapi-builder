from http import HTTPStatus

import pytest

from openapi_builder import DocumentationOptions
from openapi_builder.exceptions import MissingConverter


@pytest.mark.parametrize(
    "documentation_options__include_marshmallow_converters", [False]
)
@pytest.mark.parametrize(
    "documentation_options__strict_mode",
    [DocumentationOptions.StrictMode.FAIL_ON_ERROR],
)
@pytest.mark.usefixtures("post_with_marshmallow_input_schema")
def test_request_content_type(open_api_documentation):
    with pytest.raises(MissingConverter):
        open_api_documentation.app.try_trigger_before_first_request_functions()
