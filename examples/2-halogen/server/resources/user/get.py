from http import HTTPStatus

from flask import jsonify

from openapi_builder import add_documentation

from ...models import User
from .blueprint import blueprint
from .schema import ErrorSchema, UserSchema


@blueprint.route("/<int:user_id>")
@add_documentation(
    responses={
        HTTPStatus.OK: UserSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
    },
)
def get(user_id):
    """Provides details about a single user."""
    user = User.from_id(user_id)
    if user is None:
        return (
            jsonify(ErrorSchema.serialize({"message": "User is not found"})),
            HTTPStatus.NOT_FOUND,
        )
    return jsonify(UserSchema.serialize(user))
