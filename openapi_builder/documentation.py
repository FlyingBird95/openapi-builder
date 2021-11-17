from typing import Any, Dict, List, Optional, Union

from openapi_builder.specification import Parameter


class SwaggerDocumentation:
    def __init__(
        self,
        responses: Optional[Dict[Union[str, int], Any]] = None,
        input_schema: Optional[Any] = None,
        parameters: Optional[List[Parameter]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.responses = (
            {str(k): v for k, v in responses.items()} if responses is not None else {}
        )
        self.input_schema = input_schema
        self.parameters = parameters if parameters is not None else []
        self.summary = summary
        self.description = description
