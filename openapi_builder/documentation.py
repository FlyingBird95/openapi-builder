import contextlib
import functools
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.exceptions import MissingConfigContext
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
        self.tags = tags if tags is not None else []


class DocumentationContext:
    def __init__(self):
        self.config: Optional[Documentation] = None

    @contextlib.contextmanager
    def use_config(self, documentation_config: Documentation):
        """Context manager for function that need to be executed with a documentation_config."""
        if not isinstance(documentation_config, Documentation):
            raise TypeError(
                f"{documentation_config} is not an instance of Documentation."
            )

        self.config = documentation_config
        yield
        self.config = None

    def verify_context(self, function_to_check):
        """Verifies that the function is executed within the documentation context.

        The function must be called according to the following usage:
        >>> @documentation_context.verify_context
        >>> def process():
        >>>     ...
        """

        @functools.wraps(function_to_check)
        def inner(*args, **kwargs):
            if not isinstance(self.config, Documentation):
                raise MissingConfigContext()

            return function_to_check(*args, **kwargs)

        return inner
