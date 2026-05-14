"""Topbar component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton


class IHTopbar(ttk.Frame):
    """Horizontal top application bar."""

    def __init__(self, master=None, title: str = "", on_toggle_theme=None, **kwargs):
        super().__init__(master, padding=(18, 12), style="IH.Topbar.TFrame", **kwargs)
        ttk.Label(self, text=title, style="IH.CardTitle.TLabel").pack(side="left")
        if on_toggle_theme:
            IHButton(self, text="Tema", variant="success", outline=True, command=on_toggle_theme).pack(side="right")

