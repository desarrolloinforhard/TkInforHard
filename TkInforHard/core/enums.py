"""Shared enumerations for component APIs."""

from enum import StrEnum


class IHVariant(StrEnum):
    """Semantic visual variants supported by TkInforHard widgets."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    LIGHT = "light"
    DARK = "dark"


class IHSize(StrEnum):
    """Common component sizes."""

    SM = "sm"
    MD = "md"
    LG = "lg"

