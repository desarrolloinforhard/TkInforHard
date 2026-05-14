"""Divider component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHDivider(ttk.Separator):
    """Themed separator used between sections."""

    def __init__(self, master=None, orient: str = "horizontal", **kwargs):
        super().__init__(master, orient=orient, **kwargs)

