"""Canvas-backed sidebar navigation item."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens


class IHMenuItem(ttk.Frame):
    """Sidebar item with canvas-rounded background, icon slot and active state."""

    WIDTH = 158
    HEIGHT = 46
    RADIUS = 14
    ICON_X = 16
    TEXT_X = 50

    def __init__(
        self,
        master=None,
        text: str = "",
        icon=None,
        active: bool = False,
        command=None,
        width: int = WIDTH,
        **kwargs,
    ):
        self.text = text
        self.icon = icon
        self.active = active
        self.command = command
        self.hovered = False
        self.item_width = width
        self._tokens = self._resolve_tokens()
        super().__init__(master, width=width, height=self.HEIGHT, style="IH.Sidebar.TFrame", **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=self.HEIGHT,
            bg=self._tokens["navigation"]["sidebar_bg"],
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            takefocus=True,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<space>", self._on_keyboard_invoke)
        self.canvas.bind("<Return>", self._on_keyboard_invoke)
        self.bind("<<IHThemeChanged>>", self._on_theme_changed, add="+")
        self._draw()

    def set_active(self, active: bool) -> None:
        """Set whether the item is the active navigation entry."""

        self.active = active
        self._draw()

    def invoke(self):
        """Invoke the navigation command."""

        if self.command:
            return self.command()
        return None

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _draw_rounded_rect(self, width: int, height: int, fill: str) -> None:
        x1, y1, x2, y2 = 2, 2, width - 2, height - 2
        radius = self.RADIUS
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
        self.canvas.create_polygon(points, smooth=True, splinesteps=24, fill=fill, outline="")

    def _draw(self, _event=None) -> None:
        self._tokens = self._resolve_tokens()
        nav = self._tokens["navigation"]
        width = max(self.canvas.winfo_width(), self.item_width)
        height = max(self.canvas.winfo_height(), self.HEIGHT)
        fill = nav["item_active"] if self.active else nav["item_hover"] if self.hovered else nav["item"]
        text_color = nav["text_active"] if self.active else nav["text"]
        self.canvas.delete("all")
        self.canvas.configure(background=nav["sidebar_bg"])
        self._draw_rounded_rect(width, height, fill)
        if self.icon is not None:
            self.canvas.create_image(self.ICON_X, height / 2, image=self.icon, anchor="w")
        text_x = self.TEXT_X if self.icon is not None else 16
        self.canvas.create_text(
            text_x,
            height / 2,
            text=self.text,
            fill=text_color,
            font=(self._tokens["font"]["family"], 10, "bold"),
            anchor="w",
        )

    def _on_enter(self, _event=None) -> None:
        self.hovered = True
        self._draw()

    def _on_leave(self, _event=None) -> None:
        self.hovered = False
        self._draw()

    def _on_click(self, _event=None) -> None:
        self.canvas.focus_set()
        self.invoke()

    def _on_keyboard_invoke(self, _event=None) -> str:
        self.invoke()
        return "break"

    def _on_theme_changed(self, _event=None) -> None:
        self._draw()
