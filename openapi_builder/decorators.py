from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.constants import HIDDEN_ATTR_NAME
from openapi_builder.documentation import Documentation, SchemaOptions
from openapi_builder.specification import Parameter


def add_documentation(
    responses: Optional[Dict[Union[HTTPStatus, int], Any]] = None,
    input_schema: Optional[Any] = None,
    query_schema: Optional[Any] = None,
    parameters: Optional[List[Parameter]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
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
    """

    def inner(func):
        value = Documentation(
            responses=responses,
            input_schema=input_schema,
            query_schema=query_schema,
            parameters=parameters,
            summary=summary,
            description=description,
            tags=tags,
        )
        setattr(func, HIDDEN_ATTR_NAME, value)
        return func

    return inner


def documentation_schema_options(**options):
    """Adds schema options for a given class.

    Usage:
    >>> from marshmallow import fields
    >>>
    >>>
    >>> @documentation_schema_options(
    >>>    attr={"example": "abc"},
    >>> )
    >>> class YourSchema:
    >>>     attr = fields.Str()
    >>>     ...
    """

    def inner(func):
        value = SchemaOptions(**options)
        setattr(func, HIDDEN_ATTR_NAME, value)
        return func

    return inner
