from http import HTTPStatus

from flask import jsonify

from openapi_builder import add_documentation

from ...models import user_storage
from .blueprint import blueprint
from .schema import UserSchema


@blueprint.route("/")
@add_documentation(responses={HTTPStatus.OK: UserSchema(many=True)})
def collection():
    """Provides a collection of all users."""
    return jsonify(UserSchema(many=True).dump(user_storage))
