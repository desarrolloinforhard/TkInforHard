"""Section header component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHSectionHeader(ttk.Frame):
    """Section title with optional supporting text."""

    def __init__(self, master=None, title: str = "", subtitle: str | None = None, **kwargs):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        ttk.Label(self, text=title, style="IH.Title.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self, text=subtitle, style="IH.Muted.TLabel").pack(anchor="w", pady=(2, 0))

