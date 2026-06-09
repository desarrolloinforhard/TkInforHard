"""TkInforHard UI framework.

Reusable desktop component library built on top of tkinter, ttk and
ttkbootstrap for Inforhard internal applications.
"""

from TkInforHard.core.app import IHApplication
from TkInforHard.core.config import IHConfig
from TkInforHard.components import IHBusyOverlay, IHLoader
from TkInforHard.theme.manager import ThemeManager
from TkInforHard.utils import draw_rounded_rect
from TkInforHard.widgets import *
from TkInforHard.layout import *

__version__ = "1.1.0"

__all__ = [
    "IHApplication",
    "IHConfig",
    "ThemeManager",
    "IHBusyOverlay",
    "IHLoader",
    "IHStatusCard",
    "RoundedTableview",
    "IHTimeline",
    "IHKanbanBoard",
    "IHChatConversation",
    "draw_rounded_rect",
]


