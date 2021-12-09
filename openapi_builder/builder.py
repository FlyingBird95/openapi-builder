import re
from typing import List, Optional

from flask import Flask

from . import util
from .blueprint.blueprint import openapi_documentation
from .converters.base import Converter
from .documentation import Documentation
from .exceptions import MissingConverter
from .specification import (
    Info,
    MediaType,
    OpenAPI,
    Operation,
    Parameter,
    PathItem,
    Paths,
    RequestBody,
    Response,
    Responses,
    Schema,
    Server,
)


class DocumentationOptions:
    def __init__(
        self,
        include_head_response: bool = True,
        include_options_response: bool = True,
        server_url: str = "/",
        include_marshmallow_converters: bool = True,
        include_documentation_blueprint: bool = True,
    ):
        self.include_head_response: bool = include_head_response
        self.include_options_response: bool = include_options_response
        self.server_url: str = server_url
        self.include_marshmallow_converters: bool = include_marshmallow_converters
        self.include_documentation_blueprint: bool = include_documentation_blueprint


class OpenApiDocumentation:
    """OpenAPI Documentation builder for your Flask REST API.

    Tow ways to use the OpenApiDocumentation:

    Option 1: This is binding the instance to a specific Flask application:
    >>> app = Flask(__name__)
    >>> documentation = OpenApiDocumentation(app=app)

    Option 2: Create the object once and configure the application later to support it:
    >>> documentation = OpenApiDocumentation()
    >>> app = Flask(__name__)
    >>> documentation.init_app(app=app)

    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        title: str = "Open API REST documentation",
        version: str = "1.0.0",
        options: Optional[DocumentationOptions] = None,
    ):
        self.app: Optional[Flask] = app
        """After self.init_app is called, the self.app must not be None anymore."""

        self.specification = OpenAPI(
            info=Info(title=title, version=version),
            paths=Paths(),
            servers=[Server(url=options.server_url)],
        )
        """The specification that is generated using the builder."""

        self.options: DocumentationOptions = (
            options if options is not None else DocumentationOptions()
        )
        """Global documentation options for the builder."""

        self.builder = OpenAPIBuilder(open_api_documentation=self)
        """The builder used for iterating the endpoints. This is done in order to generate the
        configuration configuration."""

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialises the application."""
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask app instance.")

        if self.options.include_documentation_blueprint:
            app.register_blueprint(openapi_documentation)

        app.before_first_request(self.builder.iterate_endpoints)

        # Register the extension in the app.
        app.extensions["__open_api_doc__"] = self
        self.app = app

    def get_configuration(self):
        """Returns the OpenAPI configuration specification as a dictionary."""
        return self.specification.get_value()


class OpenAPIBuilder:
    """OpenAPI builder for generating the documentation."""

    def __init__(self, open_api_documentation: OpenApiDocumentation):
        self.converters: List[Converter] = []
        self.open_api_documentation: OpenApiDocumentation = open_api_documentation

        if self.options.include_marshmallow_converters:
            # Keep import below to support packages without marshmallow.
            from openapi_builder.converters.marshmallow import (
                register_marshmallow_converters,
            )

            register_marshmallow_converters(self)

    def process(self, value):
        """Processes an instance, and returns a schema, or reference to that schema."""
        converter = next(
            (
                converter
                for converter in self.converters
                if isinstance(value, converter.converts_class)
            ),
            None,
        )
        if converter is None:
            raise MissingConverter(value=value)

        return converter.convert(value=value)

    def iterate_endpoints(self):
        """Iterates the endpoints of the Flask application to generate the documentation.

        This function is executed before the first request is processed in the corresponding
        Flask application.
        """
        for rule in self.open_api_documentation.app.url_map._rules:
            view_func = self.open_api_documentation.app.view_functions[rule.endpoint]
            config: Documentation = getattr(view_func, "__open_api_doc__", None)
            if config is None:
                # endpoint has no documentation configuration -> skip
                continue

            parameters = list(config.parameters)
            parameters.extend(util.parse_openapi_arguments(rule))
            endpoint_name = util.openapi_endpoint_name_from_rule(rule)

            if endpoint_name not in self.paths.values:
                self.paths.values[endpoint_name] = PathItem(parameters=parameters)
            path_item = self.paths.values[endpoint_name]

            for method in rule.methods:
                values = {}
                for key, schema in config.responses.items():
                    reference = self.process(schema)
                    values[key] = Response(
                        description=config.description or view_func.__doc__,
                        content={"application/json": MediaType(schema=reference)},
                    )

                if config.input_schema is not None:
                    schema_or_reference = self.process(config.input_schema)
                    request_body = RequestBody(
                        description=config.description,
                        content={
                            "application/json": MediaType(schema=schema_or_reference)
                        },
                    )
                else:
                    request_body = None

                operation = Operation(
                    summary=config.summary,
                    description=config.description,
                    responses=Responses(values=values),
                    request_body=request_body,
                )

                if method == "GET":
                    path_item.get = operation
                if method == "HEAD" and self.options.include_head_response:
                    path_item.head = operation
                if method == "OPTIONS" and self.options.include_options_response:
                    path_item.options = operation
                if method == "POST":
                    path_item.post = operation
                if method == "PUT":
                    path_item.put = operation

    def register_converter(self, converter):
        """Register a converter for this builder."""
        self.converters.append(converter)

    @property
    def schemas(self):
        """Helper property to return the schemas."""
        return self.open_api_documentation.specification.components.schemas

    @property
    def paths(self):
        """Helper property to return the schemas."""
        return self.open_api_documentation.specification.paths

    @property
    def options(self):
        """Helper property to return the options."""
        return self.open_api_documentation.options
