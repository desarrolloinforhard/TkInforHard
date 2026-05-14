"""Breadcrumb component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHBreadcrumb(ttk.Frame):
    """Simple breadcrumb trail."""

    def __init__(self, master=None, items: list[str] | tuple[str, ...] = (), separator: str = "/", **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        text = f" {separator} ".join(items)
        ttk.Label(self, text=text, style="IH.CardMuted.TLabel").pack(anchor="w")

