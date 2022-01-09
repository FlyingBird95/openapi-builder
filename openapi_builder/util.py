import re


def openapi_endpoint_name_from_rule(rule):
    """Utility function to generate the Open API endpoint name.

    It replace '/users/<user_id>' with the OpenAPI standard: '/users/{user_id}'.
    """
    name = rule.rule

    for argument in rule.arguments:
        openapi_name = f"{{{argument}}}"
        name = re.sub(fr"<[a-zA-Z:]*{argument}>", openapi_name, name)

    return name
