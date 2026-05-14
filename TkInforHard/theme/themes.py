"""ttkbootstrap theme metadata.

The dictionaries follow ttkbootstrap's user theme format closely while the
runtime manager also maps them to stable bundled themes as a compatibility
fallback.
"""

from TkInforHard.theme import palette

THEMES = {
    "inforhard_dark": {
        "type": "dark",
        "base_theme": "darkly",
        "colors": {
            "primary": palette.PRIMARY,
            "secondary": palette.GRAY_500,
            "success": palette.SUCCESS,
            "info": palette.INFO,
            "warning": palette.WARNING,
            "danger": palette.DANGER,
            "light": palette.GRAY_100,
            "dark": palette.DARK_BACKGROUND,
            "bg": palette.DARK_BACKGROUND,
            "fg": palette.DARK_TEXT,
            "selectbg": palette.PRIMARY,
            "selectfg": palette.DARK_TEXT,
            "border": palette.DARK_BORDER,
            "inputfg": palette.DARK_TEXT,
            "inputbg": palette.DARK_SURFACE_ALT,
            "active": palette.DARK_SURFACE_ALT,
        },
    },
    "inforhard_light": {
        "type": "light",
        "base_theme": "flatly",
        "colors": {
            "primary": palette.PRIMARY,
            "secondary": palette.GRAY_500,
            "success": palette.SUCCESS,
            "info": palette.INFO,
            "warning": palette.WARNING,
            "danger": palette.DANGER,
            "light": palette.GRAY_50,
            "dark": palette.GRAY_900,
            "bg": palette.LIGHT_BACKGROUND,
            "fg": palette.LIGHT_TEXT,
            "selectbg": palette.PRIMARY,
            "selectfg": palette.GRAY_50,
            "border": palette.LIGHT_BORDER,
            "inputfg": palette.LIGHT_TEXT,
            "inputbg": palette.LIGHT_SURFACE,
            "active": palette.LIGHT_SURFACE_ALT,
        },
    },
}


def bootstrap_theme_for(theme_name: str) -> str:
    """Return the bundled ttkbootstrap base theme for a TkInforHard theme."""

    return THEMES.get(theme_name, THEMES["inforhard_dark"])["base_theme"]

