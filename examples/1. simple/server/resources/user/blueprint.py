from flask import Blueprint

blueprint = Blueprint(
    name="users",
    import_name=__name__,
    url_prefix="/users",
)

from . import collection, get, post, put  # noqa: F401
