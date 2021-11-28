import re
from typing import Optional

from flask import current_app

from openapi_builder.documentation import SwaggerDocumentation
from openapi_builder.processors.marshmallow import register_marshmallow_processors
from openapi_builder.specification import (
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
    ):
        self.include_head_response: bool = include_head_response
        self.include_options_response: bool = include_options_response
        self.server_url: str = server_url
        self.include_marshmallow_processors: bool = include_marshmallow_processors


class OpenAPIBuilder:
    """OpenAPI builder for generating the documentation."""

    def __init__(
        self, title: str, version: str, options: Optional[DocumentationOptions] = None
    ):
        self.specification = OpenAPI(
            info=Info(title=title, version=version),
            paths=Paths(),
            servers=[Server(url=options.server_url)],
        )
        self.processors = []
        self.options: DocumentationOptions = (
            options if options is not None else DocumentationOptions()
        )
        if self.options.include_marshmallow_processors:
            register_marshmallow_processors(self)

    def get_value(self):
        return self.specification.get_value()

    def process(self, value):
        processor = next(
            (
                processor
                for processor in self.processors
                if isinstance(value, processor.processes_class)
            ),
            None,
        )
        if processor is None:
            raise ValueError(f"No processor registered for {value}")

        return processor.process(value=value, builder=self)

    def iterate_endpoints(self):
        for rule in current_app.url_map._rules:
            view_func = current_app.view_functions[rule.endpoint]
            config: SwaggerDocumentation = getattr(view_func, "__swagger_doc__", None)
            if config is None:
                # endpoint has no documentation configuration -> skip
                continue

            parameters = list(config.parameters)
            parameters.extend(self.parse_openapi_arguments(rule))
            endpoint_name = self.openapi_endpoint_name_from_rule(rule)

            if endpoint_name not in self.specification.paths.values:
                self.specification.paths.values[endpoint_name] = PathItem(
                    parameters=parameters
                )
            path_item = self.specification.paths.values[endpoint_name]

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
                if method == "HEAD" and self.options.include_head_response:
                    path_item.head = operation
                if method == "OPTIONS" and self.options.include_options_response:
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
