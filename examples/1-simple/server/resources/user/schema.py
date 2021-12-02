from marshmallow import Schema, fields


class RegisterUser(Schema):
    """Deserialize register user schema."""

    email = fields.Email(required=True)
    """Email."""

    first_name = fields.String(required=True)
    """First name."""

    last_name = fields.String(required=True)
    """Last name."""

    password = fields.String(required=True)
    """Password."""


class UpdateUser(Schema):
    """Deserialize update user schema."""

    first_name = fields.String(required=False)
    """First name."""

    last_name = fields.String(required=False)
    """Last name."""

    password = fields.String(required=False)
    """Password."""


class UserSchema(Schema):
    """User response schema."""

    id = fields.Integer()
    """ID."""

    email = fields.Email()
    """Email."""

    first_name = fields.String()
    """First name."""

    last_name = fields.String()
    """Last name."""

    register_date = fields.DateTime()
    """Register date."""


class ErrorSchema(Schema):
    """Error response schema."""

    message = fields.String()
    """The error message."""
