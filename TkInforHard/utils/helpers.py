"""General helper functions."""


def coalesce(value, fallback):
    """Return fallback when value is None."""

    return fallback if value is None else value

