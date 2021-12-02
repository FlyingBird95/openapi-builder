import os

from flask import Blueprint

TEMPLATE_FOLDER = os.path.abspath(os.path.join(__file__, "..", "..", "templates"))

openapi_documentation = Blueprint(
    name="openapi_documentation",
    import_name=__name__,
    url_prefix="/documentation",
    template_folder=TEMPLATE_FOLDER,
)

from . import configuration, get  # noqa: F401
