from http import HTTPStatus

from flask import jsonify

from openapi_builder import add_documentation
from openapi_builder.specification import Schema

from ...models import User
from .blueprint import blueprint
from .schema import ErrorSchema, FunctionSchema, UserSchema


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
            jsonify(ErrorSchema().dump({"message": "User is not found"})),
            HTTPStatus.NOT_FOUND,
        )
    return jsonify(UserSchema().dump(user))


@blueprint.route("/custom")
@add_documentation(
    responses={HTTPStatus.OK: FunctionSchema},
    custom_converters={
        "FunctionSchema.list_of_strings": Schema(
            type="array", items=Schema(type="string")
        ),
    },
)
def custom():
    return jsonify(FunctionSchema().dump(None))
