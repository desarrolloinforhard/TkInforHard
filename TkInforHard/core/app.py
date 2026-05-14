"""Application shell for projects that consume TkInforHard."""

from __future__ import annotations

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover - fallback for partial environments
    import tkinter as tk
    from tkinter import ttk  # type: ignore

from TkInforHard.core.config import IHConfig
from TkInforHard.theme.manager import ThemeManager
from TkInforHard.theme.themes import bootstrap_theme_for


class IHApplication(ttk.Window):
    """Top-level ttkbootstrap window with the TkInforHard theme engine wired in."""

    def __init__(self, config: IHConfig | None = None, **kwargs):
        self.config_model = config or IHConfig()
        super().__init__(themename=bootstrap_theme_for(self.config_model.theme), **kwargs)
        self.title(self.config_model.title)
        self.geometry(f"{self.config_model.width}x{self.config_model.height}")
        self.minsize(self.config_model.min_width, self.config_model.min_height)
        self.resizable(self.config_model.resizable, self.config_model.resizable)
        self.theme_manager = ThemeManager(self)
        self.theme_manager.apply_theme(self.config_model.theme)

    def toggle_theme(self) -> str:
        """Toggle between inforhard dark and light themes."""

        return self.theme_manager.toggle_theme()
