from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.constants import HIDDEN_ATTR_NAME
from openapi_builder.documentation import Documentation, SchemaOptions
from openapi_builder.specification import Parameter

_MISSING = object()


def add_documentation(
    responses: Optional[Dict[Union[HTTPStatus, int], Any]] = _MISSING,
    input_schema: Optional[Any] = _MISSING,
    query_schema: Optional[Any] = _MISSING,
    parameters: Optional[List[Parameter]] = _MISSING,
    summary: Optional[str] = _MISSING,
    description: Optional[str] = _MISSING,
    tags: Optional[List[str]] = _MISSING,
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
        kwargs = {}
        if responses is not _MISSING:
            kwargs["responses"] = responses
        if input_schema is not _MISSING:
            kwargs["input_schema"] = input_schema
        if query_schema is not _MISSING:
            kwargs["query_schema"] = query_schema
        if parameters is not _MISSING:
            kwargs["parameters"] = parameters
        if summary is not _MISSING:
            kwargs["summary"] = summary
        if description is not _MISSING:
            kwargs["description"] = description
        if tags is not _MISSING:
            kwargs["tags"] = tags

        value = Documentation(**kwargs)
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
