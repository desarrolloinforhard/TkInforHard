"""Badge component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHBadge(ttk.Label):
    """Compact status label."""

    def __init__(self, master=None, text: str = "", variant: str = "success", **kwargs):
        kwargs.setdefault("bootstyle", f"{variant}-inverse")
        super().__init__(master, text=text, padding=(8, 4), **kwargs)
        self.variant = variant

