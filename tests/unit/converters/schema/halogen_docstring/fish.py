"""The purpose of this file is to define a schema by importing halogen directly."""
import halogen


class Fish(halogen.Schema):
    """Fish schema."""

    name = halogen.Attr(halogen.types.String())
    """The name of the fish."""

    age = halogen.Attr(halogen.types.Int())
    """The age of the fish in years."""
