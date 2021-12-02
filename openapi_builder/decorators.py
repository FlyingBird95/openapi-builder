from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.documentation import Documentation
from openapi_builder.specification import Parameter


def add_documentation(
    responses: Optional[Dict[Union[HTTPStatus, int], Any]] = None,
    input_schema: Optional[Any] = None,
    parameters: Optional[List[Parameter]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
):
    def inner(func):
        func.__open_api_doc__ = Documentation(
            responses=responses,
            input_schema=input_schema,
            parameters=parameters,
            summary=summary,
            description=description,
        )
        return func

    return inner
