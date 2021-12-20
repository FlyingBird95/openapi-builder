from flask import Flask

from openapi_builder import DocumentationOptions, OpenApiDocumentation

# Import blueprints
from .resources.user.blueprint import blueprint as blueprint_user

documentation = OpenApiDocumentation(
    title="REST API documentation",
    version="1.0.0",
    options=DocumentationOptions(
        include_options_response=False,
        include_head_response=False,
        include_marshmallow_converters=False,
        include_halogen_converters=True,
        server_url="/",
    ),
)


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(blueprint_user)

    # Register extensions
    documentation.init_app(app)

    return app


app = create_app()
