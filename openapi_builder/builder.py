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
    Response,
    Responses,
    Server,
)


class DocumentationOptions:
    def __init__(
        self,
        include_head_response: bool = True,
        include_options_response: bool = True,
        server_url: str = "/",
    ):
        self.include_head_response: bool = include_head_response
        self.include_options_response: bool = include_options_response
        self.server_url: str = server_url


class SwaggerBuilder:
    """Swagger builder for generating the documentation."""

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
            config: SwaggerDocumentation = getattr(
                current_app.view_functions[rule.endpoint], "__swagger_doc__", None
            )
            if config is None:
                continue

            parameters = list(config.parameters)
            for name in rule.arguments:
                parameters.append(Parameter(name=name, in_="path", required=True))

            path_item = PathItem(parameters=parameters)
            for method in rule.methods:
                values = {}
                for key, schema in config.responses.items():
                    reference = self.process(schema)
                    values[key] = Response(
                        description=config.description,
                        content={"application/json": MediaType(schema=reference)},
                    )

                operation = Operation(
                    summary=config.summary,
                    description=config.description,
                    responses=Responses(values=values),
                )

                if method == "GET":
                    path_item.get = operation
                if method == "HEAD" and self.options.include_head_response:
                    path_item.head = operation
                if method == "OPTIONS" and self.options.include_options_response:
                    path_item.options = operation

            self.specification.paths.values[rule.rule] = path_item
