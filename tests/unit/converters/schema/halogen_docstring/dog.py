"""Test schema created by importing the properties from halogen (import from)."""
from halogen import Schema, Attr, types


class Dog(Schema):
    """Dog schema."""

    name = Attr(types.String())
    """The name of the dog."""

    age = Attr(types.Int())
    """The age of the dog in years."""
