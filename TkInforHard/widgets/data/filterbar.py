"""Filter bar component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton
from TkInforHard.widgets.inputs.search_input import IHSearchInput


class IHFilterBar(ttk.Frame):
    """Horizontal filter area with search and refresh actions."""

    def __init__(self, master=None, on_search=None, on_refresh=None, **kwargs):
        super().__init__(master, padding=(0, 0, 0, 12), style="IH.Surface.TFrame", **kwargs)
        self.search = IHSearchInput(self)
        self.search.pack(side="left", fill="x", expand=True)
        IHButton(self, text="Buscar", variant="success", command=on_search).pack(side="left", padx=(8, 0))
        IHButton(self, text="Actualizar", variant="secondary", outline=True, command=on_refresh).pack(side="left", padx=(8, 0))

