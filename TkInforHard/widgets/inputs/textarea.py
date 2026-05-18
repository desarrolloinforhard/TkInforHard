"""Textarea component."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens


class IHTextArea(ttk.Frame):
    """Multiline text area with rounded canvas frame and focus state."""

    def __init__(self, master=None, label: str | None = None, height: int = 5, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame")
        self.focused = False
        self.hovered = False
        self._tokens = self._resolve_tokens()
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 5))
        self.canvas = tk.Canvas(self, height=max(height * 22, 96), highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.text = tk.Text(
            self,
            height=height,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            wrap="word",
            font=(self._tokens["font"]["family"], 10),
            **kwargs,
        )
        self.window_id = self.canvas.create_window(12, 12, anchor="nw", window=self.text)
        self.canvas.bind("<Configure>", self._draw)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.text.bind("<FocusIn>", self._on_focus_in)
        self.text.bind("<FocusOut>", self._on_focus_out)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        self._draw()

    def get(self) -> str:
        """Return the text content."""

        return self.text.get("1.0", "end-1c")

    def set(self, value: str) -> None:
        """Replace the text content."""

        self.text.delete("1.0", "end")
        self.text.insert("1.0", value)

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _surface_colors(self) -> tuple[str, str]:
        token = self._tokens["input"]
        if self.focused:
            return token["background"], token["border_focus"]
        if self.hovered:
            return token["background_hover"], token["border_hover"]
        return token["background"], token["border"]

    def _draw(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 96)
        fill, outline = self._surface_colors()
        x1, y1, x2, y2 = 1, 1, width - 2, height - 2
        radius = 12
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        self.canvas.delete("all")
        self.canvas.configure(background=self._tokens["color"]["surface"])
        self.canvas.create_polygon(points, smooth=True, splinesteps=24, fill=fill, outline=outline, width=1)
        self.window_id = self.canvas.create_window(12, 12, anchor="nw", window=self.text, width=max(width - 24, 20), height=max(height - 24, 20))
        self.text.configure(bg=fill, fg=self._tokens["color"]["text"], insertbackground=self._tokens["color"]["text"])

    def _on_enter(self, _event=None) -> None:
        self.hovered = True
        self._draw()

    def _on_leave(self, _event=None) -> None:
        self.hovered = False
        self._draw()

    def _on_focus_in(self, _event=None) -> None:
        self.focused = True
        self._draw()

    def _on_focus_out(self, _event=None) -> None:
        self.focused = False
        self._draw()

    def _on_theme_changed(self, _event=None) -> None:
        self._draw()
