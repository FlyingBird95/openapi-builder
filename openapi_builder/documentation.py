from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.specification import Parameter, Schema


class Documentation:
    """Class for storing documentation configuration.

    The preferred way to add documentation for and endpoint is via the decorator, since the default
    values are defined in the decorator.

    See `openapi_builder.decorators.add_documentation` for more info.
    """

    def __init__(
        self,
        responses: Optional[Dict[Union[HTTPStatus, int], Any]],
        input_schema: Optional[Any],
        parameters: Optional[List[Parameter]],
        summary: Optional[str],
        description: Optional[str],
        custom_converters: Optional[Dict[str, Schema]],
        tags: Optional[List[str]],
    ):
        self.responses = (
            {str(int(k)): v for k, v in responses.items()}
            if responses is not None
            else {}
        )
        self.input_schema = input_schema
        self.parameters = parameters if parameters is not None else []
        self.summary = summary
        self.description = description
        self.custom_converters = (
            custom_converters if custom_converters is not None else {}
        )
        self.tags = tags if tags is not None else []
