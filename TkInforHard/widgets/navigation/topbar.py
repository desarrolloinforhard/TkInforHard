"""Topbar component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton


class IHTopbar(ttk.Frame):
    """Horizontal top application bar."""

    def __init__(self, master=None, title: str = "", on_toggle_theme=None, on_toggle_menu=None, **kwargs):
        super().__init__(master, padding=(18, 12), style="IH.Topbar.TFrame", **kwargs)
        if on_toggle_menu:
            IHButton(self, text="Menu", variant="topbar_button", outline=True, command=on_toggle_menu).pack(side="left", padx=(0, 12))
        self._title_label = ttk.Label(self, text=title, style="IH.TopbarTitle.TLabel")
        self._title_label.pack(side="left")
        if on_toggle_theme:
            IHButton(self, text="Tema", variant="topbar_button", outline=True, command=on_toggle_theme).pack(side="right")

    def set_title(self, title: str) -> None:
        self._title_label.configure(text=title)
