from typing import TYPE_CHECKING, Union

import marshmallow

from openapi_builder.parsers.docstring import DocStringParser
from openapi_builder.processors.base import Processor
from openapi_builder.specification import Reference, Schema

if TYPE_CHECKING:
    from openapi_builder.builder import OpenAPIBuilder


class EmailProcessor(Processor):
    processes_class = marshmallow.fields.Email

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="string", format="email")


class StringProcessor(Processor):
    processes_class = marshmallow.fields.String

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="string", format="string")


class BooleanProcessor(Processor):
    processes_class = marshmallow.fields.Boolean

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="boolean", format="boolean")


class NumberProcessor(Processor):
    processes_class = marshmallow.fields.Number

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="number", format="number")


class DateProcessor(Processor):
    processes_class = marshmallow.fields.Date

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="string", format="date")


class DateTimeProcessor(Processor):
    processes_class = marshmallow.fields.DateTime

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="string", format="date-time")


class NestedProcessor(Processor):
    processes_class = marshmallow.fields.Nested

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Union[Schema, Reference]:
        schema = builder.process(value.nested)
        if value.many:
            schema = Schema(
                type="array", items=schema
            )  # TODO: replace with ListProcessor
        return schema


class ListProcessor(Processor):
    processes_class = marshmallow.fields.List

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="array", items=None)


class SchemaMetaProcessor(Processor):
    processes_class = marshmallow.schema.SchemaMeta

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        schema_name = value.__name__  # class name
        parser = DocStringParser.from_class(value)
        parser.parse()
        properties = {
            key: builder.process(value=prop)
            for key, prop in value._declared_fields.items()
        }
        for key, value in properties.items():
            if isinstance(value, Schema):
                value.description = parser.result.get(f"{schema_name}.{key}")
        schema = Schema(
            type="object",
            description=parser.result.get(schema_name),
            properties=properties,
        )
        builder.specification.components.schemas[schema_name] = schema
        return Reference.from_schema(schema_name=schema_name)


class SchemaProcessor(Processor):
    processes_class = marshmallow.schema.Schema

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        schema_name = value.__class__.__name__  # class name
        properties = {
            key: builder.process(value=prop)
            for key, prop in value._declared_fields.items()
        }

        schema = Schema(type="object", properties=properties)
        builder.specification.components.schemas[schema_name] = schema
        return Reference.from_schema(schema_name=schema_name)


class DictProcessor(Processor):
    processes_class = marshmallow.fields.Dict

    @staticmethod
    def process(value, builder: "OpenAPIBuilder") -> Schema:
        return Schema(type="object")


def register_marshmallow_processors(root_builder):
    root_builder.processors.append(EmailProcessor())
    root_builder.processors.append(StringProcessor())
    root_builder.processors.append(BooleanProcessor())
    root_builder.processors.append(NumberProcessor())
    root_builder.processors.append(DateProcessor())
    root_builder.processors.append(DateTimeProcessor())
    root_builder.processors.append(NestedProcessor())
    root_builder.processors.append(ListProcessor())
    root_builder.processors.append(SchemaProcessor())
    root_builder.processors.append(SchemaMetaProcessor())
    root_builder.processors.append(DictProcessor())
