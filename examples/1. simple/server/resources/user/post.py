from http import HTTPStatus

from flask import jsonify, request
from marshmallow.exceptions import ValidationError

from openapi_builder import add_documentation

from ...models import User, get_free_user_id
from .blueprint import blueprint
from .schema import ErrorSchema, RegisterUser, UserSchema


@blueprint.route("/", methods=["POST"])
@add_documentation(
    responses={
        HTTPStatus.CREATED: UserSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
    input_schema=RegisterUser,
)
def post():
    """Register a new user."""
    free_user_id = get_free_user_id()
    try:
        data = RegisterUser().loads(request.data)
    except ValidationError as e:
        return jsonify(ErrorSchema().dump({"message": e})), HTTPStatus.BAD_REQUEST

    user = User(
        id=free_user_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        password=data["password"],
        email=data["email"],
    )
    user.save()
    return UserSchema().dumps(user), HTTPStatus.CREATED
