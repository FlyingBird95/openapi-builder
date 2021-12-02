from http import HTTPStatus

from flask import jsonify, request
from marshmallow import ValidationError

from openapi_builder import add_documentation

from ...models import User
from .blueprint import blueprint
from .schema import ErrorSchema, UpdateUser, UserSchema


@blueprint.route("/<user_id>", methods=["PUT"])
@add_documentation(
    responses={
        HTTPStatus.OK: UserSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
    input_schema=UpdateUser,
)
def put(user_id):
    user = User.from_id(user_id)
    if user is None:
        return (
            ErrorSchema().dumps({"message": "User is not found"}),
            HTTPStatus.NOT_FOUND,
        )

    try:
        data = UpdateUser().loads(request.data)
    except ValidationError as e:
        return jsonify(ErrorSchema().dump({"message": e})), HTTPStatus.BAD_REQUEST

    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    if "password" in data:
        user.password = data["password"]

    return user
