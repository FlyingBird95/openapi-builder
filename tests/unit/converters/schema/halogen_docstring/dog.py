"""Test schema created by importing the properties from halogen (import from)."""
from halogen import Schema, Attr, types


class NumLegs(Schema):
    """Class for specifying the number of legs."""

    num_legs = Attr(types.Int())
    """Number of legs for this animal."""


class Dog(NumLegs, Schema):
    """Dog schema."""

    name = Attr(types.String())
    """The name of the dog."""

    age = Attr(types.Int())
    """The age of the dog in years."""
