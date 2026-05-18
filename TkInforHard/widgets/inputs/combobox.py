"""Combobox component."""

from __future__ import annotations

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.theme.tokens import get_tokens
from TkInforHard.widgets.inputs.input import _IHInputSurface


class IHCombobox(ttk.Frame):
    """Labeled combobox with canvas-rounded input chrome."""

    def __init__(
        self,
        master=None,
        label: str | None = None,
        values: list[str] | tuple[str, ...] = (),
        variable=None,
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame")
        self.variable = variable or tk.StringVar()
        self._tokens = self._resolve_tokens()
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 5))
        self.surface = _IHInputSurface(self)
        self.surface.pack(fill="x")
        self.combobox = ttk.Combobox(self.surface, values=values, textvariable=self.variable, **kwargs)
        self.window_id = self.surface.canvas.create_window(12, 20, anchor="w", window=self.combobox)
        self.surface.canvas.bind("<Configure>", self._resize_combobox, add="+")
        self.combobox.bind("<FocusIn>", self._on_focus_in)
        self.combobox.bind("<FocusOut>", self._on_focus_out)

    def get(self) -> str:
        """Return the selected value."""

        return self.combobox.get()

    def set(self, value: str) -> None:
        """Set the selected value."""

        self.variable.set(value)

    def _resolve_theme_name(self) -> str:
        try:
            return self.winfo_toplevel().theme_manager.current_theme
        except Exception:
            return "inforhard_dark"

    def _resolve_tokens(self) -> dict:
        return get_tokens(self._resolve_theme_name())

    def _resize_combobox(self, event) -> None:
        self.surface.canvas.itemconfigure(self.window_id, width=max(event.width - 24, 20))

    def _on_focus_in(self, _event=None) -> None:
        self.surface.focused = True
        self.surface._draw_surface()

    def _on_focus_out(self, _event=None) -> None:
        self.surface.focused = False
        self.surface._draw_surface()
