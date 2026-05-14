"""Responsive helpers for desktop window sizing."""


def screen_bucket(width: int) -> str:
    """Return a coarse responsive bucket for a width."""

    if width < 900:
        return "compact"
    if width < 1280:
        return "medium"
    return "wide"

