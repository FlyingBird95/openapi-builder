from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from flask import Blueprint

from openapi_builder.constants import HIDDEN_ATTR_NAME
from openapi_builder.documentation import (
    Documentation,
    DiscriminatorOptions,
    ResourceOptions,
    SchemaOptions,
)
from openapi_builder.specification import Parameter, Tag


def add_documentation(
    response: Optional[Union[Dict[Union[HTTPStatus], Any], Any]] = None,
    request_data: Optional[Any] = None,
    request_query: Optional[Any] = None,
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
        kwargs = {}
        if response is not None:
            kwargs["response"] = response
        if request_data is not None:
            kwargs["request_data"] = request_data
        if request_query is not None:
            kwargs["request_query"] = request_query
        if parameters is not None:
            kwargs["parameters"] = parameters
        if summary is not None:
            kwargs["summary"] = summary
        if description is not None:
            kwargs["description"] = description
        if tags is not None:
            kwargs["tags"] = tags

        value = Documentation(**kwargs)
        setattr(func, HIDDEN_ATTR_NAME, value)
        return func

    return inner


def set_resource_options(
    resource: Blueprint,
    tags: Optional[List[Union[str, Tag]]] = None,
):
    """Set documentation defaults on the blueprint."""
    kwargs = {}
    if tags is not None:
        kwargs["tags"] = tags
    value = ResourceOptions(**kwargs)
    setattr(resource, HIDDEN_ATTR_NAME, value)


def set_schema_options(
    schema: Any,
    options: Dict[str, Any] = None,
    discriminator: Optional[DiscriminatorOptions] = None,
):
    """Adds schema options for a given class.

    Usage:
    >>> from marshmallow import fields
    >>>
    >>>
    >>> class YourSchema:
    >>>     attr = fields.Str()
    >>>     ...
    >>>
    >>> set_schema_options(YourSchema, options={"attr": {"example": "abc"}})
    """
    kwargs = {}
    if options is not None:
        kwargs["options"] = options
    if discriminator is not None:
        kwargs["discriminator"] = discriminator

    value = SchemaOptions(**kwargs)
    setattr(schema, HIDDEN_ATTR_NAME, value)
