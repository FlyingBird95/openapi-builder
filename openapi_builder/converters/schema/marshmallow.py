from typing import Union

import marshmallow

from openapi_builder.specification import Reference, Schema

from .base import SchemaConverter


ALL_MARSHMALLOW_CONVERTER_CLASSES = []


def append_converter_class(converter_class):
    ALL_MARSHMALLOW_CONVERTER_CLASSES.append(converter_class)
    return converter_class


@append_converter_class
class EmailConverter(SchemaConverter):
    converts_class = marshmallow.fields.Email

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="email")


@append_converter_class
class StringConverter(SchemaConverter):
    converts_class = marshmallow.fields.String

    def convert(self, value, name) -> Schema:
        return Schema(type="string")


@append_converter_class
class BooleanConverter(SchemaConverter):
    converts_class = marshmallow.fields.Boolean

    def convert(self, value, name) -> Schema:
        return Schema(type="boolean")


@append_converter_class
class NumberConverter(SchemaConverter):
    converts_class = marshmallow.fields.Number

    def convert(self, value, name) -> Schema:
        return Schema(type="number")


@append_converter_class
class IntegerConverter(SchemaConverter):
    converts_class = marshmallow.fields.Integer

    def convert(self, value, name) -> Schema:
        return Schema(type="integer")


@append_converter_class
class FloatConverter(SchemaConverter):
    converts_class = marshmallow.fields.Float

    def convert(self, value, name) -> Schema:
        return Schema(type="float")


@append_converter_class
class UUIDConverter(SchemaConverter):
    converts_class = marshmallow.fields.UUID

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="uuid")


@append_converter_class
class DecimalConverter(SchemaConverter):
    converts_class = marshmallow.fields.Decimal

    def convert(self, value, name) -> Schema:
        return Schema(type="number")


@append_converter_class
class DateConverter(SchemaConverter):
    converts_class = marshmallow.fields.Date

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="date")


@append_converter_class
class DateTimeConverter(SchemaConverter):
    converts_class = marshmallow.fields.DateTime

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="date-time")


@append_converter_class
class TimeConverter(SchemaConverter):
    converts_class = marshmallow.fields.Time

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="time")


@append_converter_class
class URLConverter(SchemaConverter):
    converts_class = marshmallow.fields.URL

    def convert(self, value, name) -> Schema:
        return Schema(type="string", format="URL")


@append_converter_class
class NestedConverter(SchemaConverter):
    converts_class = marshmallow.fields.Nested

    def convert(self, value, name) -> Union[Schema, Reference]:
        schema = self.manager.process(value.nested, name=name)
        if value.many:
            schema = Schema(type="array", items=schema)
        return schema


@append_converter_class
class ListConverter(SchemaConverter):
    converts_class = marshmallow.fields.List

    def convert(self, value, name) -> Schema:
        return Schema(type="array", items=None)


@append_converter_class
class SchemaMetaConverter(SchemaConverter):
    converts_class = marshmallow.schema.SchemaMeta

    def convert(self, value, name) -> Schema:
        # instantiating a SchemaMeta creates a Schema
        return self.manager.process(value=value(), name=name)


@append_converter_class
class SchemaConverter(SchemaConverter):
    converts_class = marshmallow.schema.Schema

    def convert(self, value, name) -> Schema:
        schema_name = value.__class__.__name__  # class name
        properties = {
            key: self.manager.process(value=prop, name=f"{schema_name}.{key}")
            for key, prop in value._declared_fields.items()
        }

        schema = Schema(type="object", properties=properties)
        self.manager.builder.schemas[schema_name] = schema
        reference = Reference.from_schema(schema_name=schema_name, schema=schema)
        if value.many:
            return Schema(type="array", items=reference)
        return reference


@append_converter_class
class DictConverter(SchemaConverter):
    converts_class = marshmallow.fields.Dict

    def convert(self, value, name) -> Schema:
        return Schema(type="object")
