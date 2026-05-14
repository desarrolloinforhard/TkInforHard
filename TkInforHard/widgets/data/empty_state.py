"""Empty state component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHEmptyState(ttk.Frame):
    """Centered placeholder for empty datasets."""

    def __init__(self, master=None, title: str = "Sin datos", message: str = "No hay registros para mostrar.", **kwargs):
        super().__init__(master, padding=32, style="IH.Card.TFrame", **kwargs)
        ttk.Label(self, text=title, style="IH.CardTitle.TLabel").pack()
        ttk.Label(self, text=message, style="IH.CardMuted.TLabel").pack(pady=(6, 0))

