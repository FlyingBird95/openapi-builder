from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.documentation import Documentation
from openapi_builder.specification import Parameter, Schema


def add_documentation(
    responses: Optional[Dict[Union[HTTPStatus, int], Any]] = None,
    input_schema: Optional[Any] = None,
    parameters: Optional[List[Parameter]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    custom_converters: Optional[Dict[str, Schema]] = None,
    tags: Optional[List[str]] = None,
):
    """Adds documentation options for a given Flask endpoint.

    Usage:
    >>> from flask import Flask
    >>> app = Flask(__name__)

    >>> @app.route("/endpoint")
    >>> @add_documentation(...)
    >>> def endpoint():
    >>>      ...


    The parameters are:
    :param responses: optional dictionary of http-status code to a given response. A converter
    must be registered for the all response classes (and attributes in this class). e.g.:
    >>> responses = {HTTPStatus.OK: SerializesSchema(many=True)}

    :param input_schema: optional schema for deserializing. A converter must be registered for the
    class (and all attributes in the class). e.g.:
    >>> input_schema = DeserializedSchema()

    :param parameters: optional list of Paremeter objects. e.g.:
    >>> parameters = [Parameter(in_="query")]

    :param summary: optional summary for the endpoint. e.g.:
    >>> summary = "A short summary of what the endpoint does."

    :param description: optional description for the endpoint, usally a bit longer e.g.:
    >>> summary = "A verbose description of what the endpoint does, describing the meaning of " +
    >>> "parameters and return attributes."

    :param custom_converters: optional dictionary for describing custom attributes within a
    serialization class. e.g. given the following class:

    >>> import marshmallow

    >>> class CustomSchema(marshmallow.Schema):
    >>>      @marshmallow.fields.Function
    >>>      def list_of_strings(self):
    >>>          return ["abc", "def"]

    Since 'list_of_strings' cannot be serialized, a custom converter should be added:
    >>> custom_converters = {
    >>>     "CustomSchema.list_of_strings": Schema(type="array", items=Schema(type="string")),
    >>> }

    :param tags: optional list of strings that represent the endpoint. e.g.:
    >>> tags = ["users"]  # a typical value is the resource name.
    """

    def inner(func):
        func.__open_api_doc__ = Documentation(
            responses=responses,
            input_schema=input_schema,
            parameters=parameters,
            summary=summary,
            description=description,
            custom_converters=custom_converters,
            tags=tags,
        )
        return func

    return inner
