import halogen

from openapi_builder.converters import Converter, register_converter
from openapi_builder.specification import Schema


class ListConverter(Converter):
    converts_class = halogen.types.List

    def convert(self, value: halogen.types.List) -> Schema:
        try:
            inner = next(value.value)
        except TypeError:
            inner = value.value[0]
        items = self.builder.process(inner)
        schema = Schema(type="array", items=items)

        if value.allow_scalar:
            return Schema(one_of=[schema, items])
        else:
            return schema


class ISODateTimeConverter(Converter):
    converts_class = halogen.types.ISODateTime

    def convert(self, value: halogen.types.ISODateTime) -> Schema:
        return Schema(type="string", format="date-time")


class ISOUTCDateTimeConverter(Converter):
    converts_class = halogen.types.ISOUTCDateTime

    def convert(self, value: halogen.types.ISOUTCDateTime) -> Schema:
        return Schema(type="string", format="date-time")


class ISOUTCDateConverter(Converter):
    converts_class = halogen.types.ISOUTCDate

    def convert(self, value: halogen.types.ISOUTCDate) -> Schema:
        return Schema(type="string", format="date")


class StringConverter(Converter):
    converts_class = halogen.types.String

    def convert(self, value: halogen.types.String) -> Schema:
        return Schema(type="string", format="string")


class IntConverter(Converter):
    converts_class = halogen.types.Int

    def convert(self, value: halogen.types.Int) -> Schema:
        return Schema(type="integer")


class BooleanConverter(Converter):
    converts_class = halogen.types.Boolean

    def convert(self, value: halogen.types.Boolean) -> Schema:
        return Schema(type="boolean")


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


class NullableConverter(Converter):
    converts_class = halogen.types.Nullable

    def convert(self, value: halogen.types.Nullable) -> Schema:
        inner = self.builder.process(value.nested_type)
        inner.required = False
        return inner


def register_halogen_converters(builder):
    register_converter(ListConverter(builder=builder))
    register_converter(ISODateTimeConverter(builder=builder))
    register_converter(ISOUTCDateTimeConverter(builder=builder))
    register_converter(StringConverter(builder=builder))
    register_converter(IntConverter(builder=builder))
    register_converter(BooleanConverter(builder=builder))
    register_converter(AmountConverter(builder=builder))
    register_converter(NullableConverter(builder=builder))
