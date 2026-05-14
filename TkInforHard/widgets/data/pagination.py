"""Pagination component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.widgets.buttons.button import IHButton


class IHPagination(ttk.Frame):
    """Small pagination control."""

    def __init__(self, master=None, page: int = 1, total_pages: int = 1, on_prev=None, on_next=None, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        IHButton(self, text="Anterior", variant="secondary", outline=True, command=on_prev).pack(side="left")
        ttk.Label(self, text=f"Pagina {page} de {total_pages}", style="IH.Surface.TLabel").pack(side="left", padx=12)
        IHButton(self, text="Siguiente", variant="secondary", outline=True, command=on_next).pack(side="left")

