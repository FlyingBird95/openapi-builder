from http import HTTPStatus

from flask import jsonify

from openapi_builder import add_documentation

from ...models import user_storage
from .blueprint import blueprint
from .schema import Users


@blueprint.route("/")
@add_documentation(responses={HTTPStatus.OK: Users})
def collection():
    """Provides a collection of all users."""
    return jsonify(Users.serialize({"users": user_storage}))
