import contextlib
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

from openapi_builder.exceptions import MissingConfigContext
from openapi_builder.specification import Discriminator, Parameter, Tag


@dataclass()
class Documentation:
    """Class for storing documentation configuration.

    The preferred way to add documentation for and endpoint is via the decorator, since the default
    values are defined in the decorator.

    See `openapi_builder.decorators.add_documentation` for more info.
    """

    response: Union[Dict[Union[HTTPStatus], Any], Any] = field(default_factory=dict)
    request_data: Any = None
    request_query: Any = None
    parameters: List[Parameter] = field(default_factory=list)
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.response, dict):
            self.response = {HTTPStatus.OK: self.response}
        self.response = {str(int(k)): v for k, v in self.response.items()}


@dataclass()
class DiscriminatorOptions:
    """Additional options for the discriminator."""

    name: str
    all_of: bool = False
    mapping: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class SchemaOptions:
    """Additional options to be serialized for a certain schema."""

    discriminator: DiscriminatorOptions
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class ResourceOptions:
    """Additional options to be serialized for a certain resource (blueprint)."""

    tags: List[Tag] = field(default_factory=list)


class DocumentationConfigManager:
    def __init__(self):
        self.config = None

    @contextlib.contextmanager
    def use_documentation_context(self, documentation_config: Documentation):
        """Context manager for function that need to be executed with a documentation_config."""
        if not isinstance(documentation_config, Documentation):
            raise TypeError(
                f"{documentation_config} is not an instance of Documentation."
            )
        if self.config is not None:
            raise ValueError(f"self.config should be None, but is {self.config}")

        self.config = documentation_config
        yield
        self.config = None

    def ensure_valid_config(self):
        """Ensures that the function is executed within the documentation context."""
        if not isinstance(self.config, Documentation):
            raise MissingConfigContext()

        return self.config
