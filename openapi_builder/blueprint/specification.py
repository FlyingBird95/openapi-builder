from flask import current_app, jsonify

from openapi_builder.constants import EXTENSION_NAME

from .blueprint import openapi_documentation


@openapi_documentation.get("/specification")
def specification():
    """Get Open API specification."""
    return jsonify(current_app.extensions[EXTENSION_NAME].get_specification())
