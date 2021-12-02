from flask import current_app, jsonify

from .blueprint import openapi_documentation


@openapi_documentation.route("/configuration", methods=["GET"])
def configuration():
    """Get Open API configuration."""
    return jsonify(current_app.extensions["__open_api_doc__"].get_configuration())
