import halogen


class RegisterUser(halogen.Schema):
    """Deserialize register user schema."""

    email = halogen.Attr(halogen.types.String())
    """Email."""

    first_name = halogen.Attr(halogen.types.String())
    """First name."""

    last_name = halogen.Attr(halogen.types.String())
    """Last name."""

    password = halogen.Attr(halogen.types.String())
    """Password."""


class UpdateUser(halogen.Schema):
    """Deserialize update user schema."""

    first_name = halogen.Attr(halogen.types.String(), required=False)
    """First name."""

    last_name = halogen.Attr(halogen.types.String(), required=False)
    """Last name."""

    password = halogen.Attr(halogen.types.String(), required=False)
    """Password."""


class UserSchema(halogen.Schema):
    """User response schema."""

    id = halogen.Attr(halogen.types.Int())
    """ID."""

    email = halogen.Attr(halogen.types.String())
    """Email."""

    first_name = halogen.Attr(halogen.types.String())
    """First name."""

    last_name = halogen.Attr(halogen.types.String())
    """Last name."""

    register_date = halogen.Attr(halogen.types.ISODateTime())
    """Register date."""


class Users(halogen.Schema):

    users = halogen.Embedded(halogen.types.List(UserSchema))
    """List of users."""


class ErrorSchema(halogen.Schema):
    """Error response schema."""

    message = halogen.Attr(halogen.types.String())
    """The error message."""
