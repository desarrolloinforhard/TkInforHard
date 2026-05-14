"""Page layout primitive."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHPage(ttk.Frame):
    """Full-page content surface with standard padding."""

    def __init__(self, master=None, padding: int = 24, **kwargs):
        super().__init__(master, padding=padding, style="IH.TFrame", **kwargs)

