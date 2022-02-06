import enum
import warnings
from dataclasses import dataclass
from typing import Any, List, Optional

from flask import Flask
from werkzeug.routing import Rule

from . import logger
from .blueprint.blueprint import openapi_documentation
from .constants import EXTENSION_NAME, HIDDEN_ATTR_NAME
from .converters.base import CONVERTER_CLASSES, Converter
from .converters.parameter.process import parse_openapi_arguments
from .documentation import Documentation, DocumentationConfigManager
from .exceptions import MissingConverter
from .specification import (
    Info,
    MediaType,
    OpenAPI,
    Operation,
    Parameter,
    PathItem,
    Reference,
    RequestBody,
    Response,
    Responses,
    Schema,
    Server,
)
from .util import openapi_endpoint_name_from_rule


@dataclass(unsafe_hash=True, frozen=True)
class DocumentationOptions:
    """Global options as defaults for the extension."""

    class StrictMode(enum.Enum):
        FAIL_ON_ERROR = enum.auto()
        SHOW_WARNINGS = enum.auto()

    include_head_response: bool = True
    include_options_response: bool = True
    server_url: str = "/"
    include_marshmallow_converters: bool = True
    include_halogen_converters: bool = False
    include_documentation_blueprint: bool = True
    strict_mode: StrictMode = StrictMode.SHOW_WARNINGS
    request_content_type: str = "application/json"
    response_content_type: str = "application/json"


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
        """Initialize the extension.

        :param app: The Flask application for iterating the endpoints to find out the documentation.
        :param title: The title of the API.
        :param version: The version of the API implementation.
        :param options: Global documentation options for the builder.
        """
        self.app: Optional[Flask] = app
        self.options: DocumentationOptions = (
            options if options is not None else DocumentationOptions()
        )
        self.specification = OpenAPI(
            info=Info(title=title, version=version),
            servers=[Server(url=self.options.server_url)],
        )
        self.builder = OpenAPIBuilder(open_api_documentation=self)

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialises the application."""
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask app instance.")

        if self.options.include_documentation_blueprint:
            app.register_blueprint(openapi_documentation)

        app.before_first_request(self.builder.register_converters)
        app.before_first_request(self.builder.iterate_endpoints)

        # Register the extension in the app.
        app.extensions[EXTENSION_NAME] = self
        self.app = app

    def get_specification(self):
        """Returns the OpenAPI configuration specification as a dictionary."""
        # TODO: validate spec
        return self.specification.get_value()


class OpenAPIBuilder:
    """OpenAPI builder for generating the documentation."""

    def __init__(self, open_api_documentation: OpenApiDocumentation):
        self.open_api_documentation: OpenApiDocumentation = open_api_documentation
        self.converters: List[Converter] = []
        self.config_manager = DocumentationConfigManager()

    def process(self, value: Any, name: str):
        """Processes an instance, and returns a schema, or reference to that schema."""
        try:
            converter = next(
                converter for converter in self.converters if converter.matches(value)
            )
        except StopIteration:
            if self.options.strict_mode == self.options.StrictMode.FAIL_ON_ERROR:
                raise MissingConverter()
            elif self.options.strict_mode == self.options.StrictMode.SHOW_WARNINGS:
                warnings.warn(f"Missing converter for: {value}: {name}", UserWarning)
                return Schema(example="<unknown>")
            else:
                raise ValueError(f"Unknown strict mode: {self.options.strict_mode}")
        else:
            return converter.convert(value=value, name=name)

    def register_converters(self):
        """Registers converts for the instance.

        This function is executed before the first request is processed the in the corresponding
        Flask application. Also before OpenApiBuilder.iterate_endpoints.
        """
        if self.options.include_marshmallow_converters:
            # Keep import below to support packages without marshmallow.
            import openapi_builder.converters.marshmallow  # noqa: F401

        if self.options.include_halogen_converters:
            # Keep import below to support packages without halogen.
            import openapi_builder.converters.halogen  # noqa: F401

        self.converters = [
            converter_class(builder=self) for converter_class in CONVERTER_CLASSES
        ]

        # register parameter converters
        import openapi_builder.converters.parameter.flask_converters  # noqa: F401

        # register default converters
        import openapi_builder.converters.defaults.default_converters  # noqa: F401

    def iterate_endpoints(self):
        """Iterates the endpoints of the Flask application to generate the documentation.

        This function is executed before the first request is processed in the corresponding
        Flask application, but after OpenApiBuilder.register_converters.
        """
        for rule in self.open_api_documentation.app.url_map._rules:
            view_func = self.open_api_documentation.app.view_functions[rule.endpoint]
            config: Documentation = getattr(view_func, HIDDEN_ATTR_NAME, None)
            if config is None:
                # endpoint has no documentation configuration -> skip
                continue

            blueprint_name = rule.endpoint.split(".")[0]
            blueprint = self.open_api_documentation.app.blueprints.get(blueprint_name)
            resource_options = getattr(blueprint, HIDDEN_ATTR_NAME, None)

            if resource_options is not None:
                tag_names = [
                    tag.name for tag in self.open_api_documentation.specification.tags
                ]
                for tag in resource_options.tags:
                    if tag.name not in tag_names:
                        self.open_api_documentation.specification.tags.append(tag)
                        self.open_api_documentation.specification.tags.sort(
                            key=lambda t: t.name
                        )

            with self.config_manager.use_documentation_context(config):
                if resource_options is not None:
                    for tag in resource_options.tags:
                        if tag.name not in self.config.tags:
                            self.config.tags.append(tag.name)

                self.process_rule(rule)

    def process_rule(self, rule: Rule):
        """Processes a Werkzeug rule."""
        logger.info(f"Processing {rule.endpoint}")
        parameters = list(self.config.parameters)
        parameters.extend(parse_openapi_arguments(rule))
        endpoint_name = openapi_endpoint_name_from_rule(rule)

        if endpoint_name not in self.paths.values:
            self.paths.values[endpoint_name] = PathItem(parameters=parameters)
        path_item = self.paths.values[endpoint_name]

        for method in rule.methods:
            values = {}
            for key, schema in self.config.responses.items():
                reference = self.process(schema, name=key)
                values[key] = Response(
                    description=self.config.description or "",
                    content={
                        self.options.response_content_type: MediaType(schema=reference)
                    },
                )

            operation = Operation(
                summary=self.config.summary,
                description=self.config.description,
                responses=Responses(values=values),
                tags=self.config.tags,
            )

            query_schema = self.config.query_schema
            if query_schema is not None:
                schema_or_reference = self.process(query_schema, name="query")
                if isinstance(schema_or_reference, Reference):
                    schema = schema_or_reference.get_schema(
                        self.open_api_documentation.specification
                    )
                else:
                    schema = schema_or_reference
                for key, value in schema.properties.items():
                    operation.parameters.append(
                        Parameter(
                            in_="query",
                            name=key,
                            schema=value,
                            required=value.required,
                        )
                    )

            input_schema = self.config.input_schema
            if input_schema is not None:
                schema_or_reference = self.process(input_schema, name="input_schema")
                operation.request_body = RequestBody(
                    description=self.config.description,
                    content={
                        self.options.request_content_type: MediaType(
                            schema=schema_or_reference
                        ),
                    },
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
            if method == "DELETE":
                path_item.delete = operation

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

    @property
    def config(self):
        self.config_manager.ensure_valid_config()
        return self.config_manager.config
