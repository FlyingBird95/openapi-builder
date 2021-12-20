from openapi_builder.constants import DOCUMENTATION_URL


class OpenApiException(Exception):
    """Base Exception."""

    def __init__(self):
        url = f"{DOCUMENTATION_URL}/exceptions.html/{self.__class__.__name__}"
        super().__init__(f"Open {url} for more info.")


class MissingConverter(OpenApiException):
    """Missing converter for the given class or instance."""


class MissingConfigContext(OpenApiException):
    """Missing config context.

    The function must be called inside the 'use_documentation_config' context manager.
    """
