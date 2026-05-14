"""Screen utilities."""


def center_geometry(width: int, height: int, screen_width: int, screen_height: int) -> str:
    """Build a centered Tk geometry string."""

    x = max((screen_width - width) // 2, 0)
    y = max((screen_height - height) // 2, 0)
    return f"{width}x{height}+{x}+{y}"

