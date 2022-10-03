"""The purpose of this file is to define a schema by importing halogen as an alias."""
import halogen as hal


class Cat(hal.Schema):
    """Cat schema."""

    @hal.Attr(hal.types.String())
    def name(self):
        """The name of the cat."""
        return "Ginger"

    age = hal.Attr(hal.types.Int())
    """The age of the cat in years."""
