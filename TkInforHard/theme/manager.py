"""Centralized theme manager for TkInforHard."""

from __future__ import annotations

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.core.constants import DARK_THEME, LIGHT_THEME
from TkInforHard.theme.styles import register_styles
from TkInforHard.theme.themes import bootstrap_theme_for
from TkInforHard.theme.tokens import get_tokens


class ThemeManager:
    """Applies, toggles and exposes the active TkInforHard design theme."""

    def __init__(self, root=None, default_theme: str = DARK_THEME):
        self.root = root
        self.current_theme = default_theme
        self.style = ttk.Style() if root is None else ttk.Style(root)

    def apply_theme(self, theme_name: str) -> str:
        """Apply a TkInforHard theme and register component styles."""

        bootstrap_theme = bootstrap_theme_for(theme_name)
        try:
            self.style.theme_use(theme_name)
        except Exception:
            self.style.theme_use(bootstrap_theme)
        self.current_theme = theme_name
        register_styles(self.style, theme_name)
        if self.root is not None:
            tokens = get_tokens(theme_name)
            try:
                self.root.configure(background=tokens["color"]["background"])
            except Exception:
                pass
        return self.current_theme

    def toggle_theme(self) -> str:
        """Toggle between light and dark themes."""

        next_theme = LIGHT_THEME if self.current_theme == DARK_THEME else DARK_THEME
        return self.apply_theme(next_theme)

    def tokens(self) -> dict:
        """Return the active theme tokens."""

        return get_tokens(self.current_theme)

