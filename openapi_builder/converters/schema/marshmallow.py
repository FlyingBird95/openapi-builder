from abc import ABC
from typing import Union

import marshmallow

from openapi_builder.specification import Reference, Schema

from .base import SchemaConverter


ALL_MARSHMALLOW_CONVERTER_CLASSES = []


def append_converter_class(converter_class):
    ALL_MARSHMALLOW_CONVERTER_CLASSES.append(converter_class)
    return converter_class


class MarshmallowConverter(SchemaConverter, ABC):
    """Additional functionalities for converting marshmallow schemas."""

    def set_additional_properties(self, schema, value):
        if value.required is False:
            schema.required = False
        if value.dump_default is not marshmallow.missing:
            schema.default = self.manager.builder.default_manager.process(
                value.dump_default
            )
        elif value.load_default is not marshmallow.missing:
            schema.default = self.manager.builder.default_manager.process(
                value.load_default
            )


@append_converter_class
class EmailConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Email

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="email")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class StringConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.String

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class BooleanConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Boolean

    def convert(self, value, name) -> Schema:
        schema = Schema(type="boolean")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class NumberConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Number

    def convert(self, value, name) -> Schema:
        schema = Schema(type="number")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class IntegerConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Integer

    def convert(self, value, name) -> Schema:
        schema = Schema(type="integer")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class FloatConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Float

    def convert(self, value, name) -> Schema:
        schema = Schema(type="float")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class UUIDConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.UUID

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="uuid")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class DecimalConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Decimal

    def convert(self, value, name) -> Schema:
        schema = Schema(type="number")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class DateConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Date

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="date")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class DateTimeConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.DateTime

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="date-time")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class TimeConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Time

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="time")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class URLConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.URL

    def convert(self, value, name) -> Schema:
        schema = Schema(type="string", format="URL")
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class NestedConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Nested

    def convert(self, value, name) -> Union[Schema, Reference]:
        schema = self.manager.process(value.nested, name=name)
        if value.many:
            schema = Schema(type="array", items=schema)
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class ListConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.List

    def convert(self, value, name) -> Schema:
        schema = Schema(type="array", items=None)
        self.set_additional_properties(schema, value)
        return schema


@append_converter_class
class SchemaMetaConverter(MarshmallowConverter):
    converts_class = marshmallow.schema.SchemaMeta

    def convert(self, value, name) -> Schema:
        # instantiating a SchemaMeta creates a Schema
        schema = self.manager.process(value=value(), name=name)
        return schema


@append_converter_class
class MarshmallowConverter(MarshmallowConverter):
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
class DictConverter(MarshmallowConverter):
    converts_class = marshmallow.fields.Dict

    def convert(self, value, name) -> Schema:
        schema = Schema(type="object")
        self.set_additional_properties(schema, value)
        return schema
