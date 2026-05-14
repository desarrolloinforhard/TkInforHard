"""Text input component."""

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHInput(ttk.Frame):
    """Labeled text entry with optional helper text."""

    def __init__(self, master=None, label: str | None = None, helper: str | None = None, variable=None, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame")
        self.variable = variable or tk.StringVar()
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 4))
        self.entry = ttk.Entry(self, textvariable=self.variable, style="IH.TEntry", **kwargs)
        self.entry.pack(fill="x")
        if helper:
            ttk.Label(self, text=helper, style="IH.CardMuted.TLabel").pack(anchor="w", pady=(4, 0))

    def get(self) -> str:
        """Return the current input value."""

        return self.variable.get()

    def set(self, value: str) -> None:
        """Replace the current input value."""

        self.variable.set(value)

