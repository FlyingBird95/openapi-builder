import re
from typing import List, Optional

from flask import Flask

from .blueprint.blueprint import openapi_documentation
from .documentation import Documentation
from .exceptions import MissingProcessor
from .processors.base import Processor
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
        include_marshmallow_processors: bool = True,
        include_documentation_blueprint: bool = True,
    ):
        self.include_head_response: bool = include_head_response
        self.include_options_response: bool = include_options_response
        self.server_url: str = server_url
        self.include_marshmallow_processors: bool = include_marshmallow_processors
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
        self.processors: List[Processor] = []
        self.open_api_documentation: OpenApiDocumentation = open_api_documentation

        if self.open_api_documentation.options.include_marshmallow_processors:
            # Keep import below to support packages without marshmallow.
            from openapi_builder.processors.marshmallow import (
                register_marshmallow_processors,
            )

            register_marshmallow_processors(self)

    def process(self, value):
        """Processes an instance, and returns a schema, or reference to that schema."""
        processor = next(
            (
                processor
                for processor in self.processors
                if isinstance(value, processor.processes_class)
            ),
            None,
        )
        if processor is None:
            raise MissingProcessor(value=value)

        return processor.process(value=value, builder=self)

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
            parameters.extend(self.parse_openapi_arguments(rule))
            endpoint_name = self.openapi_endpoint_name_from_rule(rule)

            if (
                endpoint_name
                not in self.open_api_documentation.specification.paths.values
            ):
                self.open_api_documentation.specification.paths.values[
                    endpoint_name
                ] = PathItem(parameters=parameters)
            path_item = self.open_api_documentation.specification.paths.values[
                endpoint_name
            ]

            for method in rule.methods:
                values = {}
                for key, schema in config.responses.items():
                    reference = self.process(schema)
                    values[key] = Response(
                        description=config.description or view_func.__doc__,
                        content={"application/json": MediaType(schema=reference)},
                    )

                if config.input_schema is not None:
                    reference = self.process(config.input_schema)
                    request_body = RequestBody(
                        description=config.description,
                        content={"application/json": MediaType(schema=reference)},
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
                if (
                    method == "HEAD"
                    and self.open_api_documentation.options.include_head_response
                ):
                    path_item.head = operation
                if (
                    method == "OPTIONS"
                    and self.open_api_documentation.options.include_options_response
                ):
                    path_item.options = operation
                if method == "POST":
                    path_item.post = operation
                if method == "PUT":
                    path_item.put = operation

    @staticmethod
    def openapi_endpoint_name_from_rule(rule):
        """Utility function to generate the Open API endpoint name.

        It replace '/users/<user_id>' with the OpenAPI standard: '/users/{user_id}'.
        """
        name = rule.rule

        for argument in rule.arguments:
            openapi_name = f"{{{argument}}}"
            name = re.sub(fr"<[a-zA-Z:]*{argument}>", openapi_name, name)

        return name

    @staticmethod
    def parse_openapi_arguments(rule):
        """Parsers parameter objects."""
        parameters = []

        for argument in rule.arguments:
            schema = Schema(
                type="number", format="number"
            )  # TODO: infer schema from rule.rule
            parameters.append(
                Parameter(name=argument, in_="path", required=True, schema=schema)
            )
        return parameters
