from typing import Union

import marshmallow

from openapi_builder.converters import Converter, register_converter
from openapi_builder.specification import Reference, Schema


@register_converter
class EmailConverter(Converter):
    converts_class = marshmallow.fields.Email

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="email")


@register_converter
class StringConverter(Converter):
    converts_class = marshmallow.fields.String

    def convert(self, value, name) -> Schema:
        return Schema(type="string")


@register_converter
class BooleanConverter(Converter):
    converts_class = marshmallow.fields.Boolean

    def convert(self, value, name) -> Schema:
        return Schema(type="boolean")


@register_converter
class NumberConverter(Converter):
    converts_class = marshmallow.fields.Number

    def convert(self, value, name) -> Schema:
        return Schema(type="number")


@register_converter
class IntegerConverter(Converter):
    converts_class = marshmallow.fields.Integer

    def convert(self, value, name) -> Schema:
        return Schema(type="integer")


@register_converter
class FloatConverter(Converter):
    converts_class = marshmallow.fields.Float

    def convert(self, value, name) -> Schema:
        return Schema(type="float")


@register_converter
class UUIDConverter(Converter):
    converts_class = marshmallow.fields.UUID

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="uuid")


@register_converter
class DecimalConverter(Converter):
    converts_class = marshmallow.fields.Decimal

    def convert(self, value, name) -> Schema:
        return Schema(type="number")


@register_converter
class DateConverter(Converter):
    converts_class = marshmallow.fields.Date

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="date")


@register_converter
class DateTimeConverter(Converter):
    converts_class = marshmallow.fields.DateTime

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="date-time")


@register_converter
class TimeConverter(Converter):
    converts_class = marshmallow.fields.Time

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="time")


@register_converter
class URLConverter(Converter):
    converts_class = marshmallow.fields.URL

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="URL")


@register_converter
class NestedConverter(Converter):
    converts_class = marshmallow.fields.Nested

    def convert(self, value, name) -> Union[Schema, Reference]:
        schema = self.builder.process(value.nested, name=name)
        if value.many:
            schema = Schema(type="array", items=schema)
        return schema


@register_converter
class ListConverter(Converter):
    converts_class = marshmallow.fields.List

    def convert(self, value, name) -> Schema:
        return Schema(type="array", items=None)


@register_converter
class SchemaMetaConverter(Converter):
    converts_class = marshmallow.schema.SchemaMeta

    def convert(self, value, name) -> Schema:
        # instantiating a SchemaMeta creates a Schema
        return self.builder.process(value=value(), name=name)


@register_converter
class SchemaConverter(Converter):
    converts_class = marshmallow.schema.Schema

    def convert(self, value, name) -> Schema:
        schema_name = value.__class__.__name__  # class name
        properties = {
            key: self.builder.process(value=prop, name=f"{schema_name}.{key}")
            for key, prop in value._declared_fields.items()
        }

        schema = Schema(type="object", properties=properties)
        self.builder.schemas[schema_name] = schema
        reference = Reference.from_schema(schema_name=schema_name, schema=schema)
        if value.many:
            return Schema(type="array", items=reference)
        return reference


@register_converter
class DictConverter(Converter):
    converts_class = marshmallow.fields.Dict

    def convert(self, value, name) -> Schema:
        return Schema(type="object")
