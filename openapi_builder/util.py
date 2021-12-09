import re

from openapi_builder.specification import Parameter, Schema


def to_camelcase(s):
    """Converts a snake_case string into CamelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def openapi_endpoint_name_from_rule(rule):
    """Utility function to generate the Open API endpoint name.

    It replace '/users/<user_id>' with the OpenAPI standard: '/users/{user_id}'.
    """
    name = rule.rule

    for argument in rule.arguments:
        openapi_name = f"{{{argument}}}"
        name = re.sub(fr"<[a-zA-Z:]*{argument}>", openapi_name, name)

    return name


def parse_openapi_arguments(rule):
    """Parsers parameter objects."""
    parameters = []

    for argument in rule.arguments:
        schema = Schema(type="number", format="number")  # todo: infer type from rule.
        parameters.append(
            Parameter(name=argument, in_="path", required=True, schema=schema)
        )
    return parameters
