"""TkInforHard UI framework.

Reusable desktop component library built on top of tkinter, ttk and
ttkbootstrap for Inforhard internal applications.
"""

from TkInforHard.core.app import IHApplication
from TkInforHard.core.config import IHConfig
from TkInforHard.theme.manager import ThemeManager
from TkInforHard.utils import draw_rounded_rect
from TkInforHard.widgets import *
from TkInforHard.layout import *

__version__ = "1.0.0"

__all__ = [
    "IHApplication",
    "IHConfig",
    "ThemeManager",
    "IHStatusCard",
    "RoundedTableview",
    "draw_rounded_rect",
]

