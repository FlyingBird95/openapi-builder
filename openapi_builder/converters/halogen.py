from typing import Optional

import halogen

from openapi_builder.constants import HIDDEN_ATTR_NAME
from openapi_builder.converters import Converter, register_converter
from openapi_builder.documentation import SchemaOptions
from openapi_builder.specification import Discriminator, Reference, Schema


@register_converter
class ListConverter(Converter):
    converts_class = halogen.types.List

    def convert(self, value: halogen.types.List, name) -> Schema:
        items = self.builder.process(value.item_type, name=name)
        schema = Schema(type="array", items=items)

        if value.allow_scalar:
            return Schema(one_of=[schema, items])
        else:
            return schema


@register_converter
class ISODateTimeConverter(Converter):
    converts_class = halogen.types.ISODateTime

    def convert(self, value: halogen.types.ISODateTime, name) -> Schema:
        return Schema(type="string", format="date-time")


@register_converter
class ISOUTCDateTimeConverter(Converter):
    converts_class = halogen.types.ISOUTCDateTime

    def convert(self, value: halogen.types.ISOUTCDateTime, name) -> Schema:
        return Schema(type="string", format="date-time")


@register_converter
class ISOUTCDateConverter(Converter):
    converts_class = halogen.types.ISOUTCDate

    def convert(self, value: halogen.types.ISOUTCDate, name) -> Schema:
        return Schema(type="string", format="date")


@register_converter
class StringConverter(Converter):
    converts_class = halogen.types.String

    def convert(self, value: halogen.types.String, name) -> Schema:
        return Schema(type="string")


@register_converter
class IntConverter(Converter):
    converts_class = halogen.types.Int

    def convert(self, value: halogen.types.Int, name) -> Schema:
        return Schema(type="integer")


@register_converter
class BooleanConverter(Converter):
    converts_class = halogen.types.Boolean

    def convert(self, value: halogen.types.Boolean, name) -> Schema:
        return Schema(type="boolean")


@register_converter
class AmountConverter(Converter):
    converts_class = halogen.types.Amount

    def convert(self, value: halogen.types.Amount, name) -> Schema:
        return Schema(
            type="object",
            properties={
                "amount": Schema(type="string"),
                "currency": Schema(type="string"),
            },
        )


@register_converter
class NullableConverter(Converter):
    converts_class = halogen.types.Nullable

    def convert(self, value: halogen.types.Nullable, name) -> Schema:
        inner = self.builder.process(value.nested_type, name=name)
        inner.nullable = True
        return inner


@register_converter
class LinkConverter(Converter):
    converts_class = halogen.schema._SchemaType

    def matches(self, value) -> bool:
        return super().matches(value) and value.__name__ == "LinkSchema"

    def convert(self, value, name) -> Schema:
        properties = {}

        for prop in value.__class_attrs__.values():
            properties[prop.key] = Schema(type="string", format="url", example="<url>")

        return Schema(type="object", properties=properties)


@register_converter
class CurieConverter(Converter):
    converts_class = halogen.schema._SchemaType
    currie_attributes = {"href", "name", "templated", "type"}

    def matches(self, value) -> bool:
        return (
            super().matches(value)
            and value.__class_attrs__.keys() == self.currie_attributes
        )

    def convert(self, value, name) -> Schema:
        return Schema(
            type="object",
            properties={
                "href": Schema(type="string", format="url"),
                "name": Schema(type="string"),
                "templated": Schema(type="boolean"),
                "type": Schema(type="string"),
            },
        )


@register_converter
class SchemaConverter(Converter):
    converts_class = halogen.schema._SchemaType

    def convert(self, value, name) -> Schema:
        schema_name = value.__name__
        schema_options: Optional["SchemaOptions"] = getattr(
            value, HIDDEN_ATTR_NAME, None
        )
        properties = {}

        for key, prop in value.__class_attrs__.items():
            if prop.compartment:
                if prop.compartment not in properties:
                    properties[prop.compartment] = Schema(type="object")
                result = properties[prop.compartment].properties
            else:
                result = properties

            attr = self.builder.process(
                value=prop.attr_type,
                name=f"{schema_name}.{prop.key}",
            )
            if schema_options is not None and key in schema_options.options:
                attr.options = schema_options.options[key]
            if prop.required is False:
                attr.required = False
            if hasattr(prop, "default"):
                attr.required = False
                if callable(prop.default):
                    attr.default = prop.default()
                elif hasattr(prop.default, "value"):
                    attr.default = prop.default.value
                elif prop.default is None:
                    attr.default = None
                else:
                    attr.default = prop.default
            result[prop.key] = attr

        schema = Schema(type="object", properties=properties)
        self.builder.schemas[schema_name] = schema
        if not schema_options or not schema_options.discriminator:
            return Reference.from_schema(schema_name=schema_name, schema=schema)

        # process discriminator configuration
        new_schema = Schema(type="object")
        self.builder.schemas[schema_name] = new_schema

        mapping = {
            key: self.builder.process(value=value, name=key)
            for key, value in schema_options.discriminator.mapping.items()
        }
        if schema_options.discriminator.all_of:
            for reference in mapping.values():
                s = reference.get_schema(
                    self.builder.open_api_documentation.specification
                )
                s.all_of = [schema]
        new_schema.one_of = list(mapping.values())
        new_schema.discriminator = Discriminator(
            property_name=schema_options.discriminator.name,
            mapping={key: reference.ref for key, reference in mapping.items()},
        )

        return Reference.from_schema(schema_name=schema_name, schema=new_schema)
