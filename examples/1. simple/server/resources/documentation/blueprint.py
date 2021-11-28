from flask import Blueprint

blueprint = Blueprint(
    name="docs",
    import_name=__name__,
    url_prefix="/documentation",
)

from . import configuration, get  # noqa: F401
