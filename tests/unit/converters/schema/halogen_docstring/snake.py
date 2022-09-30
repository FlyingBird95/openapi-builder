"""The purpose of this file is to define a schema using inheritance."""
import halogen


class Animal(halogen.Schema):
    """Animal schema."""

    name = halogen.Attr(halogen.types.String())
    """The name of the animal."""

    age = halogen.Attr(halogen.types.Int())
    """The age of the animal in years."""


class Snake(Animal):
    """Snake schema."""

    length = halogen.Attr(halogen.types.Int())  # Length of the snake in centimeters.
    # The comments should be ignored.


class Python(Snake):
    """Python schema for testing double inheritance."""

    is_dangerous = halogen.Attr(halogen.types.Boolean())
    """Whether this Python is dangerous."""
