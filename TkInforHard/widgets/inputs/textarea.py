"""Textarea component."""

import tkinter as tk

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHTextArea(ttk.Frame):
    """Multiline text input wrapped in a themed frame."""

    def __init__(self, master=None, label: str | None = None, height: int = 5, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame")
        if label:
            ttk.Label(self, text=label, style="IH.Surface.TLabel").pack(anchor="w", pady=(0, 4))
        self.text = tk.Text(self, height=height, relief="flat", borderwidth=1, **kwargs)
        self.text.pack(fill="both", expand=True)

    def get(self) -> str:
        """Return the text content."""

        return self.text.get("1.0", "end-1c")

    def set(self, value: str) -> None:
        """Replace the text content."""

        self.text.delete("1.0", "end")
        self.text.insert("1.0", value)

