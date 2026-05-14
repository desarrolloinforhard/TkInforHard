"""Configuration model for TkInforHard applications."""

from dataclasses import dataclass

from TkInforHard.core.constants import DEFAULT_THEME, MIN_HEIGHT, MIN_WIDTH


@dataclass(slots=True)
class IHConfig:
    """Runtime configuration used by :class:`IHApplication`."""

    title: str = "TkInforHard App"
    theme: str = DEFAULT_THEME
    width: int = 1280
    height: int = 780
    min_width: int = MIN_WIDTH
    min_height: int = MIN_HEIGHT
    resizable: bool = True

