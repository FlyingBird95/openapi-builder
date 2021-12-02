from flask import jsonify

from openapi_builder import DocumentationOptions, OpenAPIBuilder

from .blueprint import blueprint

builder = OpenAPIBuilder(
    title="Bally REST API documentation",
    version="1.0.0",
    options=DocumentationOptions(
        include_options_response=False,
        include_head_response=False,
        server_url="/",
    ),
)


@blueprint.route("/configuration", methods=["GET"])
def configuration():
    """Get Open API configuration."""
    builder.iterate_endpoints()
    return jsonify(builder.get_value())
