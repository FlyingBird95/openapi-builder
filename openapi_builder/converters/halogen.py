import halogen

from openapi_builder.converters import Converter, register_converter
from openapi_builder.specification import Reference, Schema


@register_converter
class ListConverter(Converter):
    converts_class = halogen.types.List

    def convert(self, value: halogen.types.List) -> Schema:
        items = self.builder.process(value.item_type)
        schema = Schema(type="array", items=items)

        if value.allow_scalar:
            return Schema(one_of=[schema, items])
        else:
            return schema


@register_converter
class ISODateTimeConverter(Converter):
    converts_class = halogen.types.ISODateTime

    def convert(self, value: halogen.types.ISODateTime) -> Schema:
        return Schema(type="string", format="date-time")


@register_converter
class ISOUTCDateTimeConverter(Converter):
    converts_class = halogen.types.ISOUTCDateTime

    def convert(self, value: halogen.types.ISOUTCDateTime) -> Schema:
        return Schema(type="string", format="date-time")


@register_converter
class ISOUTCDateConverter(Converter):
    converts_class = halogen.types.ISOUTCDate

    def convert(self, value: halogen.types.ISOUTCDate) -> Schema:
        return Schema(type="string", format="date")


@register_converter
class StringConverter(Converter):
    converts_class = halogen.types.String

    def convert(self, value: halogen.types.String) -> Schema:
        return Schema(type="string", format="string")


@register_converter
class IntConverter(Converter):
    converts_class = halogen.types.Int

    def convert(self, value: halogen.types.Int) -> Schema:
        return Schema(type="integer")


@register_converter
class BooleanConverter(Converter):
    converts_class = halogen.types.Boolean

    def convert(self, value: halogen.types.Boolean) -> Schema:
        return Schema(type="boolean")


@register_converter
class AmountConverter(Converter):
    converts_class = halogen.types.Amount

    def convert(self, value: halogen.types.Amount) -> Schema:
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

    def convert(self, value: halogen.types.Nullable) -> Schema:
        inner = self.builder.process(value.nested_type)
        inner.nullable = True
        return inner


@register_converter
class LinkConverter(Converter):
    converts_class = halogen.schema._SchemaType

    def matches(self, value) -> bool:
        return super().matches(value) and value.__name__ == "LinkSchema"

    def convert(self, value) -> Schema:
        properties = {}

        for prop in value.__class_attrs__.values():
            properties[prop.key] = Schema(type="string", format="url")

        return Schema(type="object", properties=properties)


@register_converter
class CurieConverter(Converter):
    converts_class = halogen.schema._SchemaType

    def matches(self, value) -> bool:
        return super().matches(value) and value.__class_attrs__.keys() == {
            "href",
            "name",
            "templated",
            "type",
        }

    def convert(self, value) -> Schema:
        return Schema(
            type="object",
            properties={
                "href": Schema(type="string", format="url"),
                "name": Schema(type="string", format="string"),
                "templated": Schema(type="boolean"),
                "type": Schema(type="string", format="string"),
            },
        )


@register_converter
class SchemaConverter(Converter):
    converts_class = halogen.schema._SchemaType

    def convert(self, value) -> Schema:
        schema_name = value.__name__
        properties = {}

        for prop in value.__class_attrs__.values():

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

        self.builder.schemas[schema_name] = Schema(type="object", properties=properties)
        return Reference.from_schema(schema_name=schema_name)
