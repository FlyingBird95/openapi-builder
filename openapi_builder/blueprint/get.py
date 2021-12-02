import json

from flask import render_template, url_for

from .blueprint import openapi_documentation


@openapi_documentation.route("/", methods=["GET"])
def index():
    """Get Open API UI page."""
    config = {
        "app_name": "OpenAPI UI",
        "dom_id": "#openapi-ui",
        "url": url_for("openapi_documentation.configuration"),
        "layout": "StandaloneLayout",
        "deepLinking": True,
    }
    return render_template("docs.html", config_json=json.dumps(config))
