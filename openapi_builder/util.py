def to_camelcase(s):
    """Converts a snake_case string into CamelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
